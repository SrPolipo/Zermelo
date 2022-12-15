from __future__ import annotations
from typing import Set, Self,Dict
#from objects import *
import json



class positionString():
    def __init__(self, representative: str) -> None:
        self.representative = self.__simplify__(representative)
        self.pos = self.__equivClass__(self.__simplify__(representative))

    def __simplify__(self,representative: str) -> str:
        """
        Simplifies a representative.
        """
        for i in ("<>","<1>","<01>","<10>","<010>"):
            representative = representative.replace(i,"")
        return representative
    
    def __equivClass__(self,representative:str) -> Set[str]:
        """
        Returns the set of symmetric positions to the representative. 
        """
        if representative == "":
            return frozenset({"","<>","<1>", "<01>","<10>","<010>"})        
        return frozenset({representative, f"<{representative[1:-1][::-1]}>"})

    def __eq__(self, __o: positionString) -> bool:
        if type(__o) == positionString:     
            if __o.representative in self.pos:
                return True
        return False
    def __repr__(self) -> str:
        return self.representative
    def __hash__(self) -> int:
        return hash((type(self),self.pos))


    


class position(positionString):
    possibilities = {
    "<0>": "",
    "000": "010",
    "<00": "<10",
    "00>": "01>",
    "101": "111",
    "<11": "<1", 
    "11>": "1>",
    "011": "0>#<1", #the # is used for spliting reasons.
    "110": "1>#<0", 
    }
    def __init__(self, representative: str, parents:Set[position] = None, dic = None) -> None:
        super().__init__(representative)
        self.__checkedLeading__ = False
        self._nim_value = "Unknown"
        self.children = set()
        self.dic = dic
        if parents:
            if type(parents) == position:
                self.parents = {parents}
                parents.__addchild__(self)
            else:
                self.parents = parents
                for parent in parents:
                    parent.__addchild__(self)
        else:
            self.parents = set()
    def __addchild__(self,child: game):
        self.children.add(child)
    def __addparent__(self,parent:position):
        self.parents.add(parent)
        parent.__addchild__(self)
    def __mexsum__(self,s: Set[int]) -> int:
        mex = 0
        while mex in s:
            mex += 1
        return mex
    @property
    def nim_value(self):
        """
        Returns the nim value of a position, computes it if it's not calculated.
        """
        if self._nim_value != "Unknown":
            return self._nim_value
        return self.__set_nim__value__()
    def __set_nim__value__(self):
        """
        Sets the nim value of a position and returns it.
        """
        if self.representative in positionString("").pos:
            return 0
        if not self.__checkedLeading__:
            self.__leadinggames__()
        self._nim_value = self.__mexsum__({child.nim_value for child in self.children})
        return self._nim_value
    def __leadingpositionstrings__(self) -> Set[str]:
        """
        Returns the games, as a set of positionStrings, a positions leads to.
        """
        leadingstrings = set()
        pos = self.representative
        for i in range(len(pos)-2):
            if pos[i:i+3] in self.possibilities.keys():
                leadingstrings.add(self.__simplify__(
                    pos[:i] + self.possibilities[pos[i:i+3]] + pos[i+3:]
                    ))
        leadinggamestrings = [set(leadingstring.split("#")) for leadingstring in leadingstrings]
        return frozenset({frozenset({positionString(decomposedString) for decomposedString in gameString}) for gameString in leadinggamestrings})
        
    def __leadinggames__(self):
        """
        Returns the leadinggames.
        """
        leadinggames = set()
        for gameset in self.__leadingpositionstrings__():
            temp = set()
            for posString in gameset:
                if posString not in self.dic.keys():
                    self.dic[posString] = position(posString.representative, dic = self.dic)
                temp.add(self.dic[posString])
            leadinggames.add(game(positions = temp,parents = self))
        self.__checkedLeading__ = True
        return leadinggames








class game():
    def __init__(self,positions = Set[position], parents:Set[position]=None) -> None:
        if type(positions) == position:
            self.positions = frozenset({positions})
        else:
            self.positions = frozenset(positions)
        self._nim_value = "Unknown"
        self._is_won = "Unknown"
        if parents:
            if type(parents) == position:
                self.parents = {parents}
                parents.__addchild__(self)
            else:
                self.parents = parents
                for parent in self.parents:
                    parent.__addchild__(self)
        else:
            self.parents = set()
        

    def __addparent__(self,parent:position):
        """
        Adds a parent to the game, and adds the game as a child to the position
        """
        parent.__addchild__(self)
        self.parents.add(parent)
    def __xorsum__(self,setOfNims: Set[int]):
        """
        Calculates the XOR sum of a set of integers.
        """
        temp = 0
        for nim_value in setOfNims:
            temp = temp^nim_value
        return temp
    @property
    def nim_value(self):
        if self._nim_value != "Unknown":
            return self._nim_value
        return self.__set_nim_value__()
    def __set_nim_value__(self):
        self._nim_value = self.__xorsum__([pos.nim_value for pos in self.positions])
        return self._nim_value
    @property
    def is_won(self):
        if self._is_won != "Unknown":
            return self._is_won
        if self._nim_value == "Unknown":
            return 0 in {pos.nim_value for pos in self.positions}
        return bool(self.nim_value)
    def __hash__(self) -> int:
        """
        Hashing of a game, notice its independence over parents.
        """
        return hash(self.positions)
    def __eq__(self, __o: object) -> bool:
        """
        Equality of games is defined through equality of positions.
        """
        if type(__o) == game:
            if __o.positions == self.positions:
                return True
        return False
    def __repr__(self) -> str:
        return " ".join([pos.__repr__() for pos in self.positions])



if __name__ == "__main__":
    dic = {}
    N = 5
    Zeros = f"<{N*'0'}>"
    initial = position(Zeros, dic = dic)
    dic[positionString(Zeros)] = initial
    print(initial,initial.nim_value)
    for pos in {positionString(f"<{i*'0'}1{(N-i-1)*'0'}>") for i in range(1,N)}:
        print(pos, dic[pos].nim_value)

        #print(f"Starting dump of {N}")
        #with open(r"C:\Users\Chebyshev\Desktop\ParityBoardGame\Objects.json","w") as outfile:
           # t={i.representative: i.nim_value for i in dic.values()}
            #json.dump(t,outfile)
        #print(f"Ended dump of {N}")
    #fastdump("Imstillyawning",{i: i.nim_value for i in dic.values()})
    #print(t:={i: i.nim_value for i in dic.values()})
    #print(t.items())
    """
    for N in range(1,50):
        N = 5
        Zeros = f"<{N*'0'}>"
        if positionString(Zeros) in dic.keys():
            initial = dic[positionString(Zeros)]
        else:
            initial = position(Zeros, dic = dic)
            dic[positionString(Zeros)] = initial
            print(initial,initial.nim_value)
        break
    t = set(dic.values())
    print(t)
    print({type(i) for i in t})
    fastdump("Imstillyawning",initial)
    t = fastload("Imstillyawning")
    print(t)
    """
    #print((t:=dic[positionString(f"<010010001001>")]), t.nim_value)
    #print((t:=dic[positionString(f"<010010000101>")]), t.nim_value)
    #print({i: i.nim_value for i in initial.children})

    
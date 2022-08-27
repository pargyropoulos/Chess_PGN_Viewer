
from ChessEngine.ChessPiece import King,Queen,Rook,Knight,Bishop,Pawn,COLOR,PIECENAME
from ChessEngine.ChessPiece import Piece,BlackUnicodes,WhiteUnicodes

class Board:
    def __init__(self) -> None:
        self.Container=[]
        self.Log=[]
        self._MoveId=0
        self.PopulateBoard()
        self.InsertLog()
        self.MovingEvent=ChessEvent()
        self.CaptureEvent=ChessEvent()
        self.PromoteEvent=ChessEvent()
        self.HideEvent=ChessEvent()


    @staticmethod
    def fileRanktoRowCol(cls,fileRank:str) -> 'tuple[int,int]':
        return (int(fileRank[1])-1,int(ord(fileRank[0])-97))

    @property
    def MoveId(self):
        return self._MoveId

    @property        
    def UnicodeBoard(self)->list:
        """Returns a 2D list of the current state of the chess board with unicode characters"""
        array=[[None for i in range(8)] for c in range(8)]
        for item in self.Container:
            #if isinstance(item,Piece) and item.IsVisible:
            array[item.Position.Row][item.Position.Col]=item.Unicode
        return array

    def PopulateBoard(self)->None:
        self.Container.clear()
        self.Log.clear()
        self.Container.append(Rook(Color=COLOR.BLACK,Row=0,Column=0))
        self.Container.append(Knight(Color=COLOR.BLACK,Row=0,Column=1))
        self.Container.append(Bishop(Color=COLOR.BLACK,Row=0,Column=2))
        self.Container.append(Queen(Color=COLOR.BLACK,Row=0,Column=3))
        self.Container.append(King(Color=COLOR.BLACK,Row=0,Column=4))
        self.Container.append(Bishop(Color=COLOR.BLACK,Row=0,Column=5))
        self.Container.append(Knight(Color=COLOR.BLACK,Row=0,Column=6))
        self.Container.append(Rook(Color=COLOR.BLACK,Row=0,Column=7))
        for col in range (0,8):
            self.Container.append(Pawn(Color=COLOR.BLACK,Row=1,Column=col))
            self.Container.append(Pawn(Color=COLOR.WHITE,Row=6,Column=col))
        self.Container.append(Rook(Color=COLOR.WHITE,Row=7,Column=0))
        self.Container.append(Knight(Color=COLOR.WHITE,Row=7,Column=1))
        self.Container.append(Bishop(Color=COLOR.WHITE,Row=7,Column=2))
        self.Container.append(Queen(Color=COLOR.WHITE,Row=7,Column=3))
        self.Container.append(King(Color=COLOR.WHITE,Row=7,Column=4))
        self.Container.append(Bishop(Color=COLOR.WHITE,Row=7,Column=5))
        self.Container.append(Knight(Color=COLOR.WHITE,Row=7,Column=6))
        self.Container.append(Rook(Color=COLOR.WHITE,Row=7,Column=7))
        self._MoveId = 0  
        print(len(self.Container))

    def InsertLog(self)->None:
        self.Log.append(self.UnicodeBoard)

    def UpDateLog(self)->None:
        self.Log[-1]=(self.UnicodeBoard)
        
    def PopState(self)->None:
        if len(self.Log)>1:
            self.Container.clear()
            self.Log.pop()
            lastState=self.Log[-1]
            for row in range(0,8):
                for column in range(0,8):
                    uniTable=lastState
                    uniItem=uniTable[row][column]
                    if uniItem==BlackUnicodes[0]:
                        self.Container.append(King(Color=COLOR.BLACK,Row=row,Column=column))
                    if uniItem==BlackUnicodes[1]:
                        self.Container.append(Queen(Color=COLOR.BLACK,Row=row,Column=column))
                    if uniItem==BlackUnicodes[2]:
                        self.Container.append(Rook(Color=COLOR.BLACK,Row=row,Column=column))
                    if uniItem==BlackUnicodes[3]:
                        self.Container.append(Bishop(Color=COLOR.BLACK,Row=row,Column=column))
                    if uniItem==BlackUnicodes[4]:
                        self.Container.append(Knight(Color=COLOR.BLACK,Row=row,Column=column))
                    if uniItem==BlackUnicodes[5]:
                        self.Container.append(Pawn(Color=COLOR.BLACK,Row=row,Column=column))
                    if uniItem==WhiteUnicodes[0]:
                        self.Container.append(King(Color=COLOR.WHITE,Row=row,Column=column))
                    if uniItem==WhiteUnicodes[1]:
                        self.Container.append(Queen(Color=COLOR.WHITE,Row=row,Column=column))
                    if uniItem==WhiteUnicodes[2]:
                        self.Container.append(Rook(Color=COLOR.WHITE,Row=row,Column=column))
                    if uniItem==WhiteUnicodes[3]:
                        self.Container.append(Bishop(Color=COLOR.WHITE,Row=row,Column=column))
                    if uniItem==WhiteUnicodes[4]:
                        self.Container.append(Knight(Color=COLOR.WHITE,Row=row,Column=column))
                    if uniItem==WhiteUnicodes[5]:
                        self.Container.append(Pawn(Color=COLOR.WHITE,Row=row,Column=column))

                                

    def MovePiece(self, Piece:str,Color:str, ToRow:int,ToCol:int,FromRow:int=None,FromCol:int=None, Capture:bool=False)-> None:
        tag=""
        tmpItem=0
        self._MoveId+=1
        if Capture:
            for item in [piece for piece in self.Container if (piece.Position.Row==ToRow and piece.Position.Col==ToCol )]:
                tmpItem=item
                break

            
        for item in [piece for piece in self.Container if str(piece)==Piece and piece.Color==Color 
                    and (piece.Position.Row==FromRow if FromRow else not None) and (piece.Position.Col==FromCol if FromCol else not None)]: 

            if [ToRow,ToCol] in item.GetValidMoves(self.UnicodeBoard):
                item.Position.Row=ToRow
                item.Position.Col=ToCol
                tag=item.Tag
                break    
        else:
            #print (item.GetValidMoves(self.UnicodeBoard))
            fromX=FromRow if FromRow!=None else "any"
            fromY=FromCol if FromCol!=None else "any"
            raise Exception (f"Move {Color} {Piece} to: ({ToRow},{ToCol}) from: ({fromX},{fromY}) is not valid!")    
        
        #raise moving event. All the event subscribers will be notified from the event handler
        self.MovingEvent( Piece,Color,ToRow=ToRow,ToCol=ToCol,Tag=tag) #,FromRow=FromRow,FromCol=FromCol
        if Capture:
            self.Container.pop(self.Container.index(tmpItem))
            self.CaptureEvent(Tag=tmpItem.Tag)
        self.InsertLog()
 
    def CapturePiece(self, Row:int,Col:int)-> None:
        for item in [piece for piece in self.Container if (piece.Position.Row==Row and piece.Position.Col==Col )]:
            #item.IsVisible=False
            self.Container.pop(self.Container.index(item))
            self.CaptureEvent(Tag=item.Tag)
            break
        else:
            raise Exception (f"No piece at ({Row},{Col})")    

    def HidePiece(self, Row:int,Col:int)-> None:
        for item in [piece for piece in self.Container if (piece.Position.Row==Row and piece.Position.Col==Col )]:
            #item.IsVisible=False
            self.Container.pop(self.Container.index(item))
            self.HideEvent(Tag=item.Tag)
            break
        else:
            raise Exception (f"No piece at ({Row},{Col})")    

    def PromotePiece(self,Row:int,Col:int,Piece:str,Color:COLOR)-> None:
        for item in [piece for piece in self.Container if (piece.Position.Row==Row and piece.Position.Col==Col)]:
            #self.CapturePiece(Row,Col)
            #self.HidePiece(Row,Col)
            color=COLOR.BLACK if Color=='BLACK' else COLOR.WHITE

            #item.IsVisible=False
            if Piece==PIECENAME.ROOK.name:
                self.Container.append(Rook(Color=color,Row=Row,Column=Col))

            if Piece==PIECENAME.KNIGHT.name:
                self.Container.append(Knight(Color=color,Row=Row,Column=Col))

            if Piece==PIECENAME.BISHOP.name:
                self.Container.append(Bishop(Color=color,Row=Row,Column=Col))

            if Piece==PIECENAME.QUEEN.name:
                self.Container.append(Queen(Color=color,Row=Row,Column=Col))

            if Piece==PIECENAME.KING.name:
                self.Container.append(King(Color=color,Row=Row,Column=Col))

            if Piece==PIECENAME.PAWN.name:
                self.Container.append(Pawn(Color=color,Row=Row,Column=Col))
            
            self.HidePiece(Row=Row,Col=Col)
            self.PromoteEvent()
            #update log, don't insert!
            #self.Log[-1]=(self.UnicodeBoard)
            self.UpDateLog()
            
            break
        else:
            raise Exception (f"No piece at ({Row},{Col})")      

    def KingKastling(self,Color:str)-> None:    
        if Color==COLOR.WHITE.name:
            _ToRow=7 
        else:
            _ToRow=0

        self.MovePiece(PIECENAME.ROOK.name,Color,ToRow=_ToRow,ToCol=5,FromRow=_ToRow)#FromCol=7

        for item in [piece for piece in self.Container if (piece.Position.Row==_ToRow and piece.Position.Col==4)]:
            tmpKing=item
            break
        
        if isinstance(tmpKing,King):
            tmpKing.Position.Col=6

        self.MovingEvent( PIECENAME.KING.name,Color,ToRow=tmpKing.Position.Row,ToCol=tmpKing.Position.Col,Tag=tmpKing.Tag)#FromCol=4

        

    def QueenKastling(self,Color:str)-> None:
        if Color==COLOR.WHITE.name:
            _ToRow=7 
        else:
            _ToRow=0

        self.MovePiece(PIECENAME.ROOK.name,Color,ToRow=_ToRow,ToCol=3,FromRow=_ToRow)

        for item in [piece for piece in self.Container if (piece.Position.Row==_ToRow and piece.Position.Col==4)]:
            tmpKing=item
            break
        
        if isinstance(tmpKing,King):
            tmpKing.Position.Col=2
        
        self.MovingEvent( PIECENAME.KING.name,Color,ToRow=tmpKing.Position.Row,ToCol=tmpKing.Position.Col,Tag=tmpKing.Tag)#FromCol=4

    
    def PrintBoard(self,*args,**kwargs):
        print("",end= "\t")     
        i=0       
        for a in range(ord("a"),ord("h")+1):
            print(f"{chr(a)}/{i}",end= "\t")
            i+=1
        print()
        
        i=0
        for _ in self.UnicodeBoard:
            print (i,end="\t")
            i+=1
            for item in _:
                print(item,end= "\t")
            print()    

class ChessEvent:
    def __init__(self):
        self.__eventhandlers = []
 
    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self
 
    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self
 
    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)




import os
import cv2
import string
import numpy as np
import time

#reference: https://github.com/YusufBerki/PyEightQueen/blob/master/board.py

COLOR_SCHEME = {
    0: {
        1: (0, 0, 0),
        0: (255, 255, 255),
    },
    1: {
        0: (181, 217, 240),
        1: (99, 136, 181)
    }
}

PIECES = {
    "queen": {"path": os.path.join('img','queen.png')}
}


def overlay_transparent(background, overlay, x, y):
    w = background.shape[1]
    h = background.shape[0]

    overlay_image = overlay[..., :4]
    mask = overlay[..., 3:] / 255.0
    background[y:y + h, x:x + w] = (1.0 - mask) * background[y:y + h, x:x + w] + mask * overlay_image
    return background

class Board(object):
    def __init__(self,size,mode = 1,cell_length = 100):
        self.size = size
        self.cell_length = cell_length
        self.mode = mode
        self.create()
    
    def create(self):
        get_row = lambda size,shift : [{"type" : (cell_index + shift) % 2, "piece" : None} for cell_index in range(size)]
        
        self.board = [get_row(self.size, _ % 2) for _ in range(self.size)]
        
        self.panel_length = self.cell_length * self.size
        self.panel = np.zeros([self.panel_length, self.panel_length,3],dtype = np.uint8)
        self.panel.fill(255)
        
        for row_index,row in enumerate(self.board):
            for col_index,col in enumerate(row):
                cell_start = (row_index * self.cell_length, col_index * self.cell_length)
                cell_end = ((row_index + 1) * self.cell_length,(col_index + 1) * self.cell_length)
                
                self.panel = cv2.rectangle(self.panel,cell_start,cell_end,COLOR_SCHEME[self.mode][col['type']],-1)
        self.panel = cv2.cvtColor(self.panel, cv2.COLOR_BGR2BGRA)
        
    def put(self,piece,cell):
        row, column = cell
        self.board[row][column]['piece'] = piece
        return True
    
    def draw(self):
        for row_index,row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if not col['piece']:
                    continue
                xmin = row_index * self.cell_length
                ymin = col_index * self.cell_length
                xmax = (row_index + 1) * self.cell_length
                ymax = (col_index + 1) * self.cell_length
                
                piece_img = self._get_piece(col['piece'])
                mask = piece_img[...,3:]/255.0
                
                self.panel[ymin:ymax, xmin:xmax] = (1.0 - mask) * self.panel[ymin:ymax, xmin:xmax] + mask * piece_img
    
    def show(self,check = 0):
        cv2.imshow("Solution", self.panel)
        if check == 0:
            cv2.waitKey(200)
        else:
            cv2.waitKey(10000)
        return None
    
    def write(self,path):
        cv2.imwrite(path,self.panel)
    
    def _get_piece(self,piece_name):
        piece = PIECES.get(piece_name,None)
        if not piece:
            raise KeyError(f"Wrong piece name. Use: {PIECES.keys()}")
        
        piece_img = piece.get('img',None)

        if piece_img is None:
            piece_path = piece['path']

            piece_img = cv2.imread(piece_path, cv2.IMREAD_UNCHANGED)
            piece_img = cv2.resize(piece_img, (self.cell_length, self.cell_length))

            PIECES[piece_name]['img'] = piece_img
        return piece_img
    
if __name__ == "__main__":
    board = Board(size = 8)
    
    board.put('queen',(1,3))
    board.put('queen', (2,5))
    
    board.draw()
    # board.write(os.path.join('/img/', 'a.png'))
    
    board.panel = cv2.putText(board.panel, f'Solution', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    
    board.show()
            
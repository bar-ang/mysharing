import sys


def addRow(matrix,row,c,size):
    for i in range(size):
        matrix[row][i] = matrix[row][i] + c;
def addCol(matrix,col,c,size):
    for i in range(size):
        matrix[i][col] = matrix[i][col] + c;

def printMatrix(matrix,size):
     for i in range(size):
        for j in range(size):
            sys.fo(str(matrix[i][j]) + "\t");
        sys.stdout.write("\n");



def RigidElimination(matrix, w):
    if w == 0:
        return;
    sum = 0;
    for i in range(1,w):
        val = matrix[w-1][i];
        sum = sum + val;
        addCol(matrix,i,-val,w);
    addCol(matrix,0,sum,w);

    sum = 0;
    for i in range(1,w):
        val = matrix[i][w-1];
        sum = sum + val;
        addRow(matrix,i,-val,w);
    addRow(matrix,0,sum,w);

    #RigidElimination(matrix,w-1);


def matrixParse(matrix,raw,size):
    row = 0;
    col = 0;
    for i in raw:
        if i == -1:
            col = col + 1;
            row = 0;
        else:
            matrix[col][row] = i;
            row = row + 1;



w = 5
mat = [[0 for x in range(w)] for y in range(w)]

matrixParse(mat,[7,  53, 183, 439, 863, -1,497, 383, 563,  79, 973, -1,287,  63, 343, 169, 583, -1,627, 343, 773, 959, 943, -1,767, 473, 103, 699, 303],w);

printMarix(mat,w);
print("\n");
RigidElimination(mat,w);
printMatrix(mat,w);
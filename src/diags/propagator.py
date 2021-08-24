class FullPropagator():
    def __init__(self,q,qbar):
        self.name = 'prop^'+q.flavor
        self.left_indices=PropIndex(q.color,q.spin)
        self.right_indices=PropIndex(qbar.color,qbar.spin)
        self.ti = q.time
        self.tf = qbar.time

    def __str__(self):
        return self.name + '(' + self.ti + ',' + self.tf + ')' + '_{' + str(self.left_indices) + ' | ' + str(self.right_indices) + '}'

    def latexStr(self):
        return self.name + '(' + self.ti.replace('t','x') + self.ti + '\\mid ' + self.tf.replace('t','x') + self.tf + ')' + '_{\\substack{' + self.left_indices.s + '\\\\' + self.left_indices.c + '}' +  '\\substack{' + self.right_indices.s + '\\\\' + self.right_indices.c + '}}'

    def __eq__(self,other):
        return self.name==other.name and self.left_indices==other.left_indices and self.right_indices==other.right_indices and self.ti==other.ti and self.tf==other.tf


class PropIndex():
    def __init__(self,c,s):
        self.c=c
        self.s=s
    def __str__(self):
        return self.c + ' ' + self.s
    def __eq__(self,other):
        return self.c==other.c and self.s==other.s

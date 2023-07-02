
import numpy as np

class Node(object):
    def __init__(self, *parents, **kargs):
        self.graph = kargs.get('graph', default_graph)
        self.need_save = kargs.get('need_save', True)
        self.gen_node_name(**kargs)

        self.parents = list(parents)
        self.children = []
        self.value = None
        self.jacobi = None

        for parent in self.parents:
            parent.children.append(self)

        self.graph.add_node(self)

    def get_parents(self):
        """
        获取本节点的父节点
        """
        return self.parents

    def get_children(self):
        """
        获取本节点的子节点
        """
        return self.children

    def gen_node_name(self, **kargs):

        self.name = kargs.get('name', '{}:{}'.format)(
            self.__class__.__name__, self.graph.node_count()
        )
        if self.graph.name_scope:
            self.name = '{}/{}'.format(self.graph.name_scope, self.name)

    def forward(self):

        for node in self.parents:
            if node.value is None:
                node.forward()
                node.compute()

    @abc.abstractmethod
    def compute(self, parent):


    @abc.abstractmethod
    def get_jacobi(self, parent):

    def backward(self, result):
        if self.jacobi is None:
            if self is result:
                self.jacobi = np.mat(np.eye(self.dimension()))
            else:
                self.jacobi = np.mat(
                    np.zeros(result.dimension(), self.dimension())
                )

                for child in self.get_children():
                    if self.child.value is not None:
                        self.jacobi += child.backward(result) * child.get_jacobi(self)
                
        return self.jacobi

    def clear_jacobi(self):

        self.jacobi = None

    def dimension(self):

        return self.value.shape[0] * self.value.shape[1]

    def shape(self):

        return self.value.shape

    def reset_value(self, recursive = True):

        self.value = None
        if recursive:
            for child in self.children:
                child.reset_value()

                



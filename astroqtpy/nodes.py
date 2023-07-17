from .base_node import QuadNode

class NbodyNode(QuadNode):
    
    def __init__(self, x_min, x_max, y_min, y_max, depth=0):
        
        super().__init__(x_min, x_max, y_min, y_max, depth)
        
        
    def generate_node_value(self):
        pass
    
    def split_node(self):
        pass
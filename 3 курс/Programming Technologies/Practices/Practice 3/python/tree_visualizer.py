from tree_node import TreeNode
from graphviz import Digraph, nohtml


class TreeVisualizer:
    @staticmethod
    def insert_node(g, tree_node):
        if tree_node:
            g.node(str(id(tree_node)), f"""<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR>
                    <TD port="left">{'<SUB><i>l</i></SUB>' if tree_node.left else ' '}</TD>
                    <TD CELLPADDING="7"><b>{tree_node.value}</b></TD>
                    <TD port="right">{'<SUB><i>r</i></SUB>' if tree_node.right else ' '}</TD></TR></TABLE>>""")
            if tree_node.left:
                TreeVisualizer.insert_node(g, tree_node.left)
                g.edge(f'{id(tree_node)}:left', str(id(tree_node.left)))
            if tree_node.right:
                TreeVisualizer.insert_node(g, tree_node.right)
                g.edge(f'{id(tree_node)}:right', str(id(tree_node.right)))


    @staticmethod
    def visualize(tree):
        name = f'tree_{tree.value if tree else None}_{id(tree)}'
        fmt = 'png'
        g = Digraph(name, format=fmt, node_attr={'shape': 'ellipse'})
        TreeVisualizer.insert_node(g, tree)
        g.render(view=True, quiet_view=True, cleanup=True, outfile=f'./pics/{name}.{fmt}')

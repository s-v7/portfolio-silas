from ai.graph.execution.art_pipeline_dag import build_art_execution_dag
import networkx as nx

g = build_art_execution_dag()

nx.nx_pydot.write_dot(g, "docs/art_execution_dag.dot")


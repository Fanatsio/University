import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass
from typing import Dict, List
from tabulate import tabulate

@dataclass
class PageRankResult:
    values: np.ndarray
    history: np.ndarray
    iterations: int
    errors: np.ndarray

class PageRankAnalyzer:
    def __init__(self):
        self.graph = self._create_graph()
        self.node_labels = ["A", "B", "C", "D", "E"]
        
    @staticmethod
    def _create_graph() -> np.ndarray:
        graph = np.array([
            [0, 1, 1, 0, 0],  # A → B, C
            [1, 0, 0, 1, 0],  # B → A, D
            [0, 0, 0, 1, 1],  # C → D, E
            [0, 0, 0, 0, 1],  # D → E
            [0, 0, 0, 0, 0]   # E → -
        ])
        return graph

    def calculate_pagerank(self, alpha: float, max_iter: int = 100, tol: float = 1e-6, handle_dangling: bool = True) -> PageRankResult:
        """Вычисление PageRank с учетом ошибок и висячих узлов"""
        n = self.graph.shape[0]
        pr = np.ones(n) / n
        col_sums = self.graph.sum(axis=0)
        dangling_nodes = (col_sums == 0)  # Определяем висячие узлы
        if np.any(dangling_nodes):
            print(f"Внимание: найдено {np.sum(dangling_nodes)} висячих узлов")

        M = self.graph / np.where(col_sums > 0, col_sums, 1)
        history = [pr.copy()]
        errors = []
        iter_count = 0

        for _ in range(max_iter):
            # Учет висячих узлов: равномерное распределение или игнорирование
            dangling_factor = np.ones(n) / n if handle_dangling else np.zeros(n)
            pr_new = (1 - alpha) / n + alpha * (M @ pr + pr @ dangling_nodes * dangling_factor)
            error = np.linalg.norm(pr_new - pr, ord=2)
            errors.append(error)
            iter_count += 1
            if error < tol:
                break
            pr = pr_new
            history.append(pr.copy())
            
        return PageRankResult(pr, np.array(history), iter_count, np.array(errors))

    def draw_graph(self) -> None:
        plt.figure(figsize=(8, 6))
        G = nx.DiGraph(self.graph)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, 
                arrowsize=20, font_size=12, font_weight='bold')
        plt.title("Структура графа ссылок", fontsize=14, pad=10)
        plt.show()

    def plot_history(self, results: Dict[float, PageRankResult]) -> None:
        n_alphas = len(results)
        cols = min(2, n_alphas)
        rows = (n_alphas + cols - 1) // cols
        fig, axs = plt.subplots(rows, cols, figsize=(15, 5 * rows), squeeze=False)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD']
        alphas = sorted(results.keys())

        for idx, alpha in enumerate(alphas):
            result = results[alpha]
            ax = axs[idx // cols, idx % cols]
            for i, label in enumerate(self.node_labels):
                ax.plot(result.history[:, i], label=f'Страница {label}',
                        color=colors[i], linewidth=2.5, marker='o', markersize=5)
            ax.set_xlabel('Итерации', fontsize=12)
            ax.set_ylabel('Значение PageRank', fontsize=12)
            ax.set_title(f'α={alpha}, {result.iterations} итераций', fontsize=14)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, linestyle='--', alpha=0.7)

        for idx in range(len(alphas), rows * cols):
            fig.delaxes(axs[idx // cols, idx % cols])

        plt.suptitle('Динамика PageRank для разных значений α', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.show()

    def print_results(self, results: Dict[float, np.ndarray]) -> None:
        alphas = sorted(results.keys())
        headers = ["Страница"] + [f"α={a}" for a in alphas]
        table_data = []
        for i, label in enumerate(self.node_labels):
            row = [label] + [f"{results[a][i]:.4f}" for a in alphas]
            table_data.append(row)
        
        print("\nРЕЗУЛЬТАТЫ PageRank")
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", floatfmt=".4f"))

    def print_analysis(self, results: Dict[float, PageRankResult]) -> None:
        print("\nАНАЛИЗ РЕЗУЛЬТАТОВ")
        print("1. Влияние структуры:")
        max_pr_node = np.argmax(results[0.85].values)
        print(f"   - Страница {self.node_labels[max_pr_node]} имеет максимальный PR "
              f"({results[0.85].values[max_pr_node]:.4f} при α=0.85) благодаря входящим ссылкам")
        print("   - Страницы без исходящих ссылок (E) аккумулируют значимость")
        print("2. Влияние α:")
        print(f"   - При α={max(results.keys())} структура графа сильно влияет "
              f"(разброс PR: {np.max(results[max(results.keys())].values) - np.min(results[max(results.keys())].values):.4f})")
        print(f"   - При α={min(results.keys())} распределение ближе к равномерному "
              f"(разброс PR: {np.max(results[min(results.keys())].values) - np.min(results[min(results.keys())].values):.4f})")

    def run_analysis(self, alphas: List[float] = [0.6, 0.7, 0.85, 0.95]) -> None:
        self.draw_graph()
        results = {}
        for alpha in alphas:
            result = self.calculate_pagerank(alpha)
            results[alpha] = result
        self.plot_history(results)
        self.print_results({alpha: result.values for alpha, result in results.items()})
        self.print_analysis(results)

analyzer = PageRankAnalyzer()
analyzer.run_analysis()
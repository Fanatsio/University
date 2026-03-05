import numpy as np
import matplotlib.pyplot as plt
from functions import f1, f2, phi

def plot_localization_phase(X1, X2, F1, F2, PHI):
    """Визуализация этапа локализации"""
    fig = plt.figure(figsize=(16, 10))
    
    # 1. График f1(x1,x2) = 0
    ax1 = fig.add_subplot(221)
    contour1 = ax1.contour(X1, X2, F1, levels=[0], colors='blue', linewidths=2)
    ax1.clabel(contour1, inline=True, fontsize=10)
    ax1.contour(X1, X2, F1, levels=20, colors='lightblue', alpha=0.5, linestyles='dashed')
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x2')
    ax1.set_title('Линии уровня f1(x1,x2) = 0 (синяя)')
    ax1.grid(True, alpha=0.3)
    
    # 2. График f2(x1,x2) = 0
    ax2 = fig.add_subplot(222)
    contour2 = ax2.contour(X1, X2, F2, levels=[0], colors='red', linewidths=2)
    ax2.clabel(contour2, inline=True, fontsize=10)
    ax2.contour(X1, X2, F2, levels=20, colors='lightcoral', alpha=0.5, linestyles='dashed')
    ax2.set_xlabel('x1')
    ax2.set_ylabel('x2')
    ax2.set_title('Линии уровня f2(x1,x2) = 0 (красная)')
    ax2.grid(True, alpha=0.3)
    
    # 3. Совмещенный график
    ax3 = fig.add_subplot(223)
    ax3.contour(X1, X2, F1, levels=[0], colors='blue', linewidths=2)
    ax3.contour(X1, X2, F2, levels=[0], colors='red', linewidths=2)
    ax3.contour(X1, X2, PHI, levels=20, cmap='viridis', alpha=0.6)
    ax3.set_xlabel('x1')
    ax3.set_ylabel('x2')
    ax3.set_title('Пересечение f1=0 (синий) и f2=0 (красный)')
    ax3.grid(True, alpha=0.3)
    
    # Легенда
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], color='blue', lw=2, label='f1(x) = 0'),
                       Line2D([0], [0], color='red', lw=2, label='f2(x) = 0')]
    ax3.legend(handles=legend_elements, loc='upper right')
    
    # 4. Тепловая карта
    ax4 = fig.add_subplot(224)
    im = ax4.imshow(PHI, extent=[X1.min(), X1.max(), X2.min(), X2.max()], 
                    origin='lower', cmap='viridis', aspect='auto', alpha=0.8)
    plt.colorbar(im, ax=ax4, label='Φ(x)')
    ax4.contour(X1, X2, PHI, levels=20, colors='white', alpha=0.5, linewidths=0.5)
    ax4.set_xlabel('x1')
    ax4.set_ylabel('x2')
    ax4.set_title('Тепловая карта Φ(x) = f1² + f2²')
    
    plt.tight_layout()
    plt.show()

def visualize_results(history, solution):
    """Визуализация процесса минимизации"""
    # Создаем сетку
    x1 = np.linspace(-2, 6, 100)
    x2 = np.linspace(-2, 4, 100)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)
    
    for i in range(len(x1)):
        for j in range(len(x2)):
            Z[j, i] = phi([X1[j, i], X2[j, i]])
    
    # 3D график
    fig = plt.figure(figsize=(15, 5))
    
    ax1 = fig.add_subplot(131, projection='3d')
    surf = ax1.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)
    ax1.scatter(history[:, 0], history[:, 1], [phi(x) for x in history], color='red', s=50)
    ax1.plot(history[:, 0], history[:, 1], [phi(x) for x in history], 'r-', linewidth=1, alpha=0.7)
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x2')
    ax1.set_zlabel('Φ(x)')
    ax1.set_title('Траектория минимизации')
    plt.colorbar(surf, ax=ax1, shrink=0.5)
    
    # 2D контурный график
    ax2 = fig.add_subplot(132)
    contour = ax2.contour(X1, X2, Z, levels=50, cmap='viridis')
    ax2.plot(history[:, 0], history[:, 1], 'r.-', linewidth=2, markersize=8)
    ax2.plot(solution[0], solution[1], 'g*', markersize=15, label='Найденный минимум')
    ax2.plot(history[0, 0], history[0, 1], 'bo', markersize=8, label='Начальное приближение')
    ax2.set_xlabel('x1')
    ax2.set_ylabel('x2')
    ax2.set_title('Траектория на контурной карте')
    ax2.legend()
    plt.colorbar(contour, ax=ax2)
    
    # График сходимости
    ax3 = fig.add_subplot(133)
    phi_values = [phi(x) for x in history]
    ax3.semilogy(range(len(phi_values)), phi_values, 'b.-')
    ax3.set_xlabel('Итерация')
    ax3.set_ylabel('Φ(x)')
    ax3.set_title('Сходимость метода')
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()
"""Static report figures, no student identifiers."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.metrics import (ConfusionMatrixDisplay, precision_recall_curve, roc_curve,
                             average_precision_score, roc_auc_score, confusion_matrix)

plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
                     'figure.facecolor': 'white', 'axes.titleweight': 'bold'})
COLORS = ['#0D5E7D', '#D6A650', '#499E8D', '#8796A4']


def save(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=170, bbox_inches='tight')
    plt.close(fig)


def eda_figures(data, directory):
    fig, ax = plt.subplots(figsize=(7, 4))
    data.risco.value_counts().reindex([0, 1]).plot.bar(ax=ax, color=COLORS[:2], rot=0)
    ax.set_xticklabels(['Alfabetizado', 'Não alfabetizado'])
    ax.set(title='Classes no treino: alunos elegíveis de 2024', ylabel='Alunos na amostra de treino')
    save(fig, directory / 'eda_classes.png')
    fig, ax = plt.subplots(figsize=(8, 4))
    data.groupby('sigla_uf').risco.mean().sort_values().plot.bar(ax=ax, color=COLORS[0])
    ax.set(title='Treino: proporção de não alfabetizados por UF', ylabel='Fração na amostra não ponderada')
    save(fig, directory / 'eda_risco_uf.png')
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    data.taxa_municipal_anterior.hist(bins=25, ax=axes[0], color=COLORS[0])
    axes[0].set(title='Contexto municipal de 2023', xlabel='Taxa de alfabetização (%)', ylabel='Alunos')
    data.log_populacao_anterior.hist(bins=25, ax=axes[1], color=COLORS[2])
    axes[1].set(title='População municipal de 2022', xlabel='log(1 + população)', ylabel='Alunos')
    save(fig, directory / 'eda_contexto.png')


def evaluation_figures(y, probability, threshold, validation_comparison, importance, directory):
    fig, ax = plt.subplots(figsize=(7, 4))
    validation_comparison.set_index('model').average_precision.plot.barh(ax=ax, color=COLORS)
    ax.set(title='Comparação somente na validação', xlabel='Average precision (risco positivo)')
    save(fig, directory / 'validation_models.png')
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    precision, recall, _ = precision_recall_curve(y, probability)
    axes[0].plot(recall, precision, color=COLORS[0],
                 label=f'AP = {average_precision_score(y, probability):.3f}')
    axes[0].set(xlabel='Recall', ylabel='Precisão')
    axes[0].axhline(np.mean(y), color=COLORS[1], ls='--', label='Prevalência')
    axes[0].set_title('Precisão-recall no teste'); axes[0].legend()
    false_positive, true_positive, _ = roc_curve(y, probability)
    axes[1].plot(false_positive, true_positive, color=COLORS[0],
                 label=f'AUC = {roc_auc_score(y, probability):.3f}')
    axes[1].plot([0,1], [0,1], '--', color=COLORS[3])
    axes[1].set(xlabel='Taxa de falsos positivos', ylabel='Taxa de verdadeiros positivos')
    axes[1].legend()
    axes[1].set_title('ROC no teste')
    save(fig, directory / 'test_curves.png')
    confusion_figure(confusion_matrix(y, probability >= threshold, labels=[0,1]),
                     directory / 'test_confusion.png')
    fig, ax = plt.subplots(figsize=(6, 4))
    observed, predicted = calibration_curve(y, probability, n_bins=10, strategy='quantile')
    ax.plot(predicted, observed, 'o-', color=COLORS[0]); ax.plot([0, 1], [0, 1], '--', color=COLORS[3])
    ax.set(title='Calibração no teste', xlabel='Risco previsto', ylabel='Fração observada')
    save(fig, directory / 'test_calibration.png')
    importance_figure(importance, directory / 'validation_importance.png')


def importance_figure(importance, path):
    fig, ax = plt.subplots(figsize=(8, 4))
    importance.sort_values('importance').plot.barh(x='feature', y='importance',
        xerr='std', legend=False, ax=ax, color=COLORS[0])
    ax.set(title='Importância por permutação na validação', xlabel='Redução de average precision', ylabel='')
    save(fig, path)


def confusion_figure(counts, path):
    fig, ax = plt.subplots(figsize=(6, 4))
    ConfusionMatrixDisplay(confusion_matrix=np.asarray(counts),
        display_labels=['Alfabetizado', 'Não alfabetizado']).plot(ax=ax, cmap='Blues', colorbar=False)
    ax.set(title='Teste: limiar escolhido na validação', xlabel='Classe prevista', ylabel='Classe observada')
    save(fig, path)

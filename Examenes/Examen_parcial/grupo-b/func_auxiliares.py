import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

#
# visualización
#

def plot_stem( t , y, y_lim=None, view_baseline=True, title=None, force_int_xaxis=False):
    """Función que configura y visualiza un gráfico stem 
       Parámetros:
       t -- muestras de tiempo
       y -- secuencia para visualizar
       y_lim -- tupla de la forma (min, max) que establece los límites en el eje de ordenadas. Por defecto None
       view_baseline -- Establece una línea horizontal en el eje de las x a la altura de  y=0 . Por defecto False
       force_int_xaxis -- Establece el eje x a valores enteros en pasos de 1 en 1 
    """
    markerline, stemlines, baseline = plt.stem(t, y,use_line_collection=True)
    if force_int_xaxis: 
        plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.setp(baseline, visible=view_baseline)
    plt.setp(markerline, color="crimson",markersize = 10)
    plt.setp(stemlines, color="crimson", linewidth = 4)
    if 0 in t:
        plt.axvline(x=0, linewidth=1,color="black")
    plt.ylim(y_lim)
    if title is not None:
        plt.title(title)
    plt.show()

# correlación

def own_correlation_lags(in1_len, in2_len):
    """Calcula el array de índices que representan los lags o desplazamientos para la correlación 1-D
        Parámetros:
        in1_len: longitud de la primera señal en la operación de correlación
        in2_len: longitud de la segunda señal en la operación de correlación
    """
    return np.arange(-in2_len + 1, in1_len)


# copiado del boletín 4

#
# objeto señal: almacenamos datos y muestras
#
class sennal():
    def __init__(self, d, t):
        self.d = np.array(d.copy())
        self.t = np.array(t.copy())

#
# señales básicas
#

# impulso básico
def sennal_impulso(t):
    return sennal(1.0*(np.array(t) == 0), t)

# escalón
def sennal_escalon(t):
    return sennal(1.0*(np.array(t) >= 0), t)

#
# bloques básicos
#

# sumador de señales
def sumador(s1, s2):
    if not isinstance(s1, sennal): raise Exception("only signals, please")
    if not isinstance(s2, sennal): raise Exception("only signals, please")
    # revisar el boletín 2
    tt = np.arange(min(s1.t[0], s2.t[0]), max(s1.t[-1], s2.t[-1])+1)
    dd = []
    for i in tt:
        v = 0.0
        if i>=s1.t[0] and i<=s1.t[-1]:
            v = v + s1.d[i-s1.t[0]]
        if i>=s2.t[0] and i<=s2.t[-1]:
            v = v + s2.d[i-s2.t[0]]
        dd.append(v)
    return sennal(dd, tt)

# retardador de señal con pérdida de datos
def retardador(s, n=0):
    if not isinstance(s, sennal): raise Exception("only signals, please")
    if not isinstance(n, int): raise Exception("should be an integer, please")
    if n < 0: raise Exception("should be a positive integer, please")
    if n >= len(s.d):
        return sennal(np.zeros(len(s.d)), s.t)
    else:
        dd = np.insert(s.d.copy(), 0, np.zeros(n))
        return sennal(dd[:len(s.d)], s.t)

# escalador de señal
def escalador(s, n=1.0):
    if not isinstance(s, sennal): raise Exception("only signals, please")
    if not isinstance(float(n), float): raise Exception("should be a number, please")
    return sennal(n*s.d, s.t)

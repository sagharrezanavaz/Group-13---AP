import matplotlib.pyplot as plt
import base64
from io import BytesIO
def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph
def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,5))
    plt.bar(x,y,color='#e28743')
    plt.xticks(rotation=45)
    plt.xlabel('date')
    plt.ylabel('sales quantity')
    plt.tight_layout()
    graph=get_graph()
    return graph
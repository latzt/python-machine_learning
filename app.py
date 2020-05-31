from flask import Flask
from flask import request
from flask import render_template

from flask_cors import CORS

import io
import sys
import yaml
import base64
import imageio
import numpy
import matplotlib.pyplot

from neuralnetwork import neuralNetwork

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return render_template('index.html')


def initNetwork() -> neuralNetwork:
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Default configuration for 28x28 pixel images.
    input_nodes = cfg.get("input_nodes", 784)
    hidden_nodes = cfg.get("hidden_nodes", 200)
    output_nodes = cfg.get("output_nodes", 10)
    learning_rate = cfg.get("learning_rate", 0.01)

    n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    if cfg.get("kernel", None):
        n.load(cfg.get("kernel"))
        print(f"loaded kernel {n.kernel_name}")

    return n


@app.route('/query', methods=['POST'])
def query():

    try:
        img_array = imageio.imread(request.data, as_gray=True)
    except ValueError as e:
        return {'message': str(e)}

    # reshape from 28x28 to list of 784 values, invert values
    img_data  = 255.0 - img_array.reshape(784)
        
    # then scale data to range from 0.01 to 1.0
    img_data = (img_data / 255.0 * 0.99) + 0.01

    print("min = ", numpy.min(img_data))
    print("max = ", numpy.max(img_data))
    assert numpy.min(img_data) > 0 and numpy.min(img_data) < 1, 'numpy.min out of acceptable input range'
    assert numpy.max(img_data) > 0 and numpy.max(img_data) <= 1, 'numpy.max out of acceptable input range'

    # query the network
    n = initNetwork()
    outputs = n.query(img_data)
    print(outputs)

    # get image data
    backquery_img_data = n.backquery(outputs.flatten().tolist())
    
    # plot image data
    plot_img = io.BytesIO()
    matplotlib.pyplot.imshow(backquery_img_data.reshape(28,28), cmap='Greys', interpolation='None')
    matplotlib.pyplot.savefig(plot_img, format='png')

    # the index of the highest value corresponds to the label
    label = numpy.argmax(outputs)
    print(f'network says {label}')
    
    return {
        'message': f'network says {label}', 
        'outputs': outputs.flatten().tolist(),
        'image': 'data:image/png;base64,' + base64.b64encode(plot_img.getvalue()).decode()
    }
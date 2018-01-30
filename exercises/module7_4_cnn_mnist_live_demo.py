# Module 7: Convolutional Neural Network (CNN)
# Live Demo on MNIST dataset

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
os.environ['TF_ENABLE_WINOGRAD_NONE_USED']='1'

import tensorflow as tf
import numpy as np
import tkinter as tk
from PIL import Image, ImageDraw, ImageFilter

class ImageGenerator:

    def __init__(self, parent, *kwargs):
        self.parent = parent
        self.posx = 10
        self.posy = 10
        self.sizex = 200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.drawing_area = tk.Canvas(self.parent, width=self.sizex, height=self.sizey)
        self.drawing_area.place(x=self.posx, y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button = tk.Button(self.parent, text="Done!", width=10, bg='white', command=self.minst_nn_pred)
        self.button.place(x=self.sizex / 7, y=self.sizey + 20)
        self.button1 = tk.Button(self.parent, text="Clear!", width=10, bg='white', command=self.clear)
        self.button1.place(x=(self.sizex / 7) + 80, y=self.sizey + 20)

        self.image = Image.new("RGB", (200, 200), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def save(self):
        img = self.image.resize((28,28)).convert('L')
        self.minst_nn_pred(img)

    def clear(self):
        self.drawing_area.delete("all")
        self.image = Image.new("RGB", (200, 200), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def b1down(self, event):
        self.b1 = "down"

    def b1up(self, event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self, event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold, self.yold, event.x, event.y, smooth='true', width=20, fill='black')
                self.draw.line(((self.xold, self.yold), (event.x, event.y)), (0, 128, 0), width=20)

        self.xold = event.x
        self.yold = event.y

    def minst_nn_pred(self):


        sess = tf.Session()
        saver = tf.train.import_meta_graph('./models/mnist_cnn/mnist_cnn.ckpt.meta')
        saver.restore(sess, tf.train.latest_checkpoint('./models/mnist_cnn'))

        graph = tf.get_default_graph()
        X = graph.get_tensor_by_name("X:0")
        yhat = graph.get_tensor_by_name("yhat:0")
        #pkeep = graph.get_tensor_by_name("pkeep:0")

        img = self.image.convert('L').resize((28, 28))
        X_test = np.asarray(img)
        X_test = X_test.astype('float32')
        X_test = (255.0 - X_test)/255.0

        # import matplotlib.pyplot as plt
        # plt.imshow(X_test,cmap='gray')
        # plt.show()

        X_test = X_test.reshape(1, 28,28,1)

        prediction = sess.run(tf.argmax(yhat,1), feed_dict={X: X_test})
        print("Predicted digit is : ", prediction)


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (250, 250, 10, 10))
    root.config(bg='white')
    ImageGenerator(root)
    root.mainloop()
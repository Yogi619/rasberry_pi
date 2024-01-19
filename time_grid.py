import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QWebView, QLabel, QScrollArea, QMainWindow
from PyQt5.QtCore import Qt, QUrl, QTimer
import requests
from bs4 import BeautifulSoup

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Multi-Pane Interface")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Google Weather Report
        weather_view = QWebView(self)
        weather_view.load(QUrl("https://www.google.com/search?q=weather"))
        layout.addWidget(weather_view)

        # Image Slideshow
        image_label = QLabel(self)
        layout.addWidget(image_label)
        self.load_images(image_label)

        # World News Scroll
        news_scroll = QScrollArea(self)
        news_label = QLabel(self)
        news_scroll.setWidgetResizable(True)
        news_scroll.setWidget(news_label)
        layout.addWidget(news_scroll)
        self.load_news(news_label)

        # Live News Channel (Example: BBC News)
        live_news_view = QWebView(self)
        live_news_view.load(QUrl("https://www.youtube.com/embed/live_stream?channel=UC16niRr50-MSBwiO3YDb3RA"))
        layout.addWidget(live_news_view)

        # Set timer to refresh news every 10 minutes
        QTimer.singleShot(600000, lambda: self.load_news(news_label))

    def load_images(self, label):
        # Add your image URLs here
        image_urls = ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
        image_index = 0

        def update_image():
            nonlocal image_index
            label.setPixmap(requests.get(image_urls[image_index]).content)
            image_index = (image_index + 1) % len(image_urls)

        update_image()
        QTimer.singleShot(5000, update_image)  # Change image every 5 seconds

    def load_news(self, label):
        # Fetch world news from a news website
        url = "https://example.com/world-news"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        news_headlines = [headline.text for headline in soup.find_all("h2")]

        # Display news in a scrolling label
        label.setText("\n".join(news_headlines))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

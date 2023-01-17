import wikipediaapi
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
# from tkinter import PhotoImage
from urllib.request import urlopen,urlretrieve
import PIL
from PIL import Image, ImageTk
import requests
import io
import os

def get_wikipedia_summary():
    try:
        topic = entry.get()
        language = lang_var.get()
        wikipedia = wikipediaapi.Wikipedia(
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page = wikipedia.page(topic)
        if page.exists():
            summary = page.summary
            text.config(state='normal')
            text.delete('1.0', END)
            text.insert(INSERT, summary)
            text.config(wrap=WORD)
            text.config(state='disabled')

    # extract the image URLs from the HTML
            soup = BeautifulSoup(page.text, 'html.parser')
            img_tags = soup.find_all('img')
            img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
            if img_urls:
                # follow redirects and add the protocol
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
                img_url = img_urls[0]
                if not img_url.startswith('http'):
                    img_url = 'http:' + img_url
                response = requests.get(img_url, headers=headers)
                if response.status_code != 200:
                    image_label.config(image='')
                    return
                # save the image to a temporary file
                img_data = response.content
                try:
                    image = Image.open(io.BytesIO(img_data))
                    photo = ImageTk.PhotoImage(image)
                    # clear the previous image
                    image_label.config(image='')
                    # update the label with the new image
                    image_label.config(image=photo)
                    image_label.image = photo
                except PIL.UnidentifiedImageError as e:
                    # handle the exception by providing a default image or message
                    image_label.config(image='')
                    text.config(state='normal')
                    text.delete('1.0', END)
                    text.insert(INSERT, "Image not found")
                    text.config(state='disabled')
            else:
                image_label.config(image='')
        else:
            text.config(state='normal')
            text.delete('1.0', END)
            text.insert(INSERT, "Page not found")
            text.config(state='disabled')
            image_label.config(image='')
    except Exception as e:
        text.config(state='normal')
        text.delete('1.0', END)
        text.insert(INSERT, f"An error occurred: {e}")
        text.config(state='disabled')
        image_label.config(image='')

def save_to_desktop():
    try:
        topic = entry.get()
        language = lang_var.get()
        wikipedia = wikipediaapi.Wikipedia(
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page = wikipedia.page(topic)
        if page.exists():
            summary = page.summary
            with open(f"{topic}.txt", "w") as file:
                file.write(summary)
            text.config(state='normal')
            text.delete('1.0', END)
            text.insert(
                INSERT, f"Summary saved to {os.path.expanduser('~')}/Desktop/{topic}.txt")
            text.config(state='disabled')
        else:
            text.config(state='normal')
            text.delete('1.0', END)
            text.insert(INSERT, "Page not found")
            text.config(state='disabled')
    except Exception as e:
        text.config(state='normal')
        text.delete('1.0', END)
        text.insert(INSERT, f"An error occurred: {e}")
        text.config(state='disabled')
        
# tkinter visuals

root = Tk()
root.title("Wikipedia Summary")

label = ttk.Label(root, text="Enter the topic you would like to learn about:")
label.pack()

entry = ttk.Entry(root)
entry.pack()

lang_var = StringVar(value='en')
lang_dropdown = ttk.OptionMenu(root, lang_var, 'en', 'fr', 'de', 'es', 'it')
lang_dropdown.pack()

text = Text(root, height=30, width=130)
text.pack()
text.config(state='disabled')

image_label = Label(root)
image_label.pack()

button = ttk.Button(root, text="Submit", command=get_wikipedia_summary)
button.pack()

root.mainloop()
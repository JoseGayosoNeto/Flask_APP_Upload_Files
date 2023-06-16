from flask import Flask, request, redirect, url_for, render_template, flash
import os


app = Flask(__name__)

app.config.from_object('config')

TIPOS_DISPONIVEIS = set(['txt', 'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'])


def arquivos_permitidos(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in TIPOS_DISPONIVEIS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=["POST"])
def upload_image():
    file = request.files['file']
    if file.filename == '':
        flash("Nenhum arquivo foi selecionado", category="file_error")
        return redirect(request.url)

    if not arquivos_permitidos(file.filename):
        flash("Utilize um tipo de arquivo permitido!", category="compatibility_error")
        return redirect(request.url)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    filename = os.path.basename(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    flash("Imagem Enviada com Sucesso", category="success")
    return render_template("index.html", filename=filename)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)



@app.route('/images_list')
def list_images():
    images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        images.append({"path": image, "basename": os.path.basename(image),
                       "format": os.path.splitext(image)[1]})
    return render_template("list.html", images=images)


if __name__ == '__main__':
    app.run(debug=True)


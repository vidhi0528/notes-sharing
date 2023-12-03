from flask import Flask,render_template,request,flash,redirect,url_for
import os
import sqlite3

app=Flask(__name__)
app.secret_key="123"
app.config['UPLOAD_FOLDER']="static\PDF"

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS Notes(pid integer primary key,pdf TEXT)"""
cursor.execute(command)
connection.close()

@app.route("/",methods=["GET","POST"])
def upload():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Notes")
    data = cur.fetchall()
    con.close()

    if request.method == 'POST':
        upload_pdf = request.files['upload_PDF']
        if upload_pdf.filename!='':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_pdf.filename)
            upload_pdf.save(filepath)
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("insert into Notes(pdf)values(?)", (upload_pdf.filename,))
            con.commit()
            flash("File Upload Successfully", "success")

            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from Notes")
            data = cur.fetchall()
            con.close()
            return render_template("upload.html", data=data)
    return render_template("upload.html",data=data)

@app.route('/update_record/<string:id>',methods=['GET','POST'])
def update_record(id):
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Notes where pid=?",(id))
    data = cur.fetchall()
    con.close()

    if request.method == 'POST':
        try:
            upload_pdf = request.files['upload_PDF']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_pdf.filename)
            upload_pdf.save(filepath)
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("UPDATE Notes SET pdf=? where pid=?", (upload_pdf.filename, id))
            con.commit()
            flash("Record Update Successfully", "success")
        except:
            flash("Record Update Failed", "danger")
        finally:
            return redirect(url_for("upload"))
            con.close()
    return render_template("update.html",data=data)

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("delete from Notes where pid=?", [id])
        con.commit()
        flash("Record Deleted Successfully", "success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("upload"))
        con.close()

if __name__ == '__main__':
    app.run(debug=True)
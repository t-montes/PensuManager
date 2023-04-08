
import tkinter as tk
from functools import partial

#CONSTANTS.

name_courses_file = 'courses_data.txt'
name_pensum_file = 'pensum_data.txt'

numSems = 10 # if file is empty, this is the number of semesters to create.

bg_color = '#D2E8ED'

#FUNCTIONS.

def x_agregarMateria_semestre(codigo:str, semestre: int) -> bool:
    with open(name_pensum_file,'r') as file:
        ls = file.readlines()
    
    with open(name_courses_file,'r') as file:
        for i in file:
            if i.split(';')[0] == codigo:
                cred = int(i.split(';')[2])
    
    line = ls[semestre].split(';')
    for i in line[1:-1]:
        if i[:i.find(':')] == codigo:
            return False
    line.insert(-1, f'{codigo}:{cred}')
    ls[semestre] = ';'.join(line)    
    
    with open(f'copy_{name_pensum_file}','w') as file:
        file.writelines(ls)
    
    with open(name_pensum_file,'w') as file:
        file.writelines(ls)
    return True

def x_registrarMateria(codigo:str, nombre:str, creditos:int, prerequisitos:list
                       ,corequisitos:list, estado:str, descripcion:str) -> bool:
    
    descripcion = descripcion.replace(';','.') # fix ';' bug

    with open(name_courses_file,'r') as file:
        ls = file.readlines()
    
    for i in ls:
        i = i.split(';')[0]
        if i == codigo:
            return False
    
    with open(f'copy_{name_courses_file}','w') as file:
        file.writelines(ls)
    
    line = '\n'
    line += f'{codigo};'
    line += f'{nombre};'
    line += f'{creditos};'
    #prerequisitos : ['MATE 1203', 'O', 'MATE 1204', 'Y', 'FISI 1018', 'Y', 'FISI 1019']
    for i in range(0,len(prerequisitos),2):
        try:
            y_o = prerequisitos[i+1]
            if y_o == 'Y' or y_o == 'y':
                line += f'{prerequisitos[i]}:'
            elif y_o == 'O' or y_o == 'o':
                line += f'{prerequisitos[i]}?'
        except IndexError:
            line += f'{prerequisitos[i]}'
    line += ';'
    for i in range(0, len(corequisitos),2):
        try:
            y_o = corequisitos[i+1]
            if y_o == 'Y' or y_o == 'y':
                line += f'{corequisitos[i]}:'
            elif y_o == 'O' or y_o == 'o':
                line += f'{corequisitos[i]}?'
        except IndexError:
            line += f'{corequisitos[i]}'
    line += ';'
    line += f'{estado};'
    descripcion = descripcion.replace('\n', ' ').replace(';', ' ')
    line += f'{descripcion}'
    
    with open(name_courses_file,'a') as file:
        file.write(line)
    return True

def agregarMateria_module(semestre: int) -> None:
    materia = f"{chgMat1Text.get('1.0','end-1c').upper()} {chgMat2Text.get('1.0','end-1c')}"
    if materia in obtener_materias():
        if not mtNueva.get():
            if x_agregarMateria_semestre(materia, semestre):
                limpiar_frame_materias()
                actualizar_frame_materias()
                limpiar_superior()
                chgAlertLabel.config(width=30, height=2)
                chgAlertLabel['text'] = f'La Materia \'{materia}\'\nha sido añadida al semestre {semestre}.'
                chgAlertLabel.place(x=50, y= 25)
                QuitButton.place(x=100, y=100)
            else:
                chgAlertLabel.config(width=11, height=5)
                chgAlertLabel['text'] = f'La Materia\n\'{materia}\'\nya está\nen el\nsemestre {semestre}.'
                chgAlertLabel.place(x=1093, y=180)
        else:
            chgAlertLabel.config(width=11, height=5)
            chgAlertLabel['text'] = f'La Materia\n\'{materia}\'\nya está\nregistrada.'
            chgAlertLabel.place(x=1093, y=180)
    else:
        if not mtNueva.get():
            chgAlertLabel.config(width=11, height=5)
            chgAlertLabel['text'] = f'La Materia\n\'{materia}\'\nno está\nregistrada.'
            chgAlertLabel.place(x=1093, y=180)
        else:
            nombre = nmNombText.get('1.0','end-1c')
            creditos = nmCredText.get('1.0','end-1c')
            pr = []
            for i in nmPre:
                if type(i) == tk.Button:
                    pr.append(i['text'].replace('\n', ' '))
                pr.append('Y')
            try:
                del pr[len(pr) - 1]
            except:
                pass
            co = []
            for i in nmCo:
                if type(i) == tk.Button:
                    co.append(i['text'].replace('\n', ' '))
                co.append('Y')
            try:
                del co[len(co) - 1]
            except:
                pass
            estado = 'Pendiente'
            descripcion = nmDescText.get('1.0','end-1c')
            
            if materia == ' ' or nombre == '' or not creditos.isdigit():
                chgAlertLabel.config(width=11, height=5)
                chgAlertLabel['text'] = f'Se deben llenar:\nDepartamento,\nNúmero,\nCréditos,\nNombre Materia.'
                chgAlertLabel.place(x=1093, y=180)
            
            elif x_registrarMateria(materia, nombre, creditos, pr, co, estado, descripcion):
                if x_agregarMateria_semestre(materia, semestre):
                    limpiar_frame_materias()
                    actualizar_frame_materias()
                    limpiar_superior()
                    chgAlertLabel.config(width=30, height=2)
                    chgAlertLabel['text'] = f'La Materia \'{materia}\'\n ha sido añadida al semestre {semestre}.'
                    chgAlertLabel.place(x=50, y= 25)
                    QuitButton.place(x=100, y=100)
                else:
                    chgAlertLabel.config(width=11, height=5)
                    chgAlertLabel['text'] = f'La Materia\n\'{materia}\'\nya está\nen el\nsemestre {semestre}.'
                    chgAlertLabel.place(x=1093, y=180)
            else:
                chgAlertLabel.config(width=11, height=5)
                chgAlertLabel['text'] = f'La Materia\n\'{materia}\'\nya está\nregistrada.'
                chgAlertLabel.place(x=1093, y=180)
    
def obtener_dptos(parcial:str) -> tuple:
    with open(name_courses_file,'r') as file:
        file.readline()
        ls = ()
        for i in file:
            dpt = i.split(';')[0][:4]
            if dpt not in ls and parcial.upper() in dpt:
                ls += (dpt,)
        return ls

def obtener_materias() -> tuple:
    with open(name_courses_file, 'r') as file:
        file.readline()
        ls = ()
        for i in file:
            ls += (i.split(';')[0],)
        return ls

def x_nm_quitar_prerequisito(codigo: str) -> None:
    for i in range(len(nmPre)):
        nmPre[i].place_forget()
        if nmPre[i]['text'].replace('\n', ' ') == codigo:
            index = i
    nmPreContx.set(810 - 38)
    del nmPre[index]
    for i in nmPre:
        i.place(x=nmPreContx.get(), y=nmPreConty.get())
        nmPreContx.set(nmPreContx.get() + 38)
        
def x_nm_agregar_prerequisito() -> None:
    materia = nmPre1Text.get('1.0', 'end-1c').upper()
    if len(materia) > 6:
        registro = False
    else:
        registro = True
    for i in nmPre:
        if i['text'].replace('\n', ' ') == materia:
            registro = True
    if not registro:
        button = tk.Button(frm, text=materia.replace(' ', '\n'), command=partial(x_nm_quitar_prerequisito,materia))
        button.config(width=4, height=2, bg=colorMateria(materia), anchor='w')
        button.place(x=nmPreContx.get(), y=nmPreConty.get())
        nmPre.append(button)
        nmPreContx.set(nmPreContx.get() + 38)
        nmPre1Text.delete('1.0', tk.END)

def x_nm_quitar_corequisito(codigo: str) -> None:
    for i in range(len(nmCo)):
        nmCo[i].place_forget()
        if nmCo[i]['text'].replace('\n', ' ') == codigo:
            index = i
    nmCoContx.set(810 - 38)
    del nmCo[index]
    for i in nmCo:
        i.place(x=nmCoContx.get(), y=nmCoConty.get())
        nmCoContx.set(nmCoContx.get() + 38)

def x_nm_agregar_corequisito() -> None:
    materia = nmCo1Text.get('1.0', 'end-1c').upper()
    if len(materia) > 6:
        registro = False
    else:
        registro = True
    for i in nmCo:
        if i['text'].replace('\n', ' ') == materia:
            registro = True
    if not registro:
        button = tk.Button(frm, text=materia.replace(' ', '\n'), command=partial(x_nm_quitar_corequisito, materia))
        button.config(width=4, height=2, bg=colorMateria(materia), anchor='w')
        button.place(x=nmCoContx.get(), y=nmCoConty.get())
        nmCo.append(button)
        nmCoContx.set(nmCoContx.get() + 38)
        nmCo1Text.delete('1.0', tk.END)

def x_quitar_materia_semestre(codigo:str, semestre:int) -> None:
    with open(name_pensum_file,'r') as file:
        ls = file.readlines()
    
    with open(f'copy_{name_pensum_file}', 'w') as file:
        file.writelines(ls)
    
    line = ls[semestre].split(';')
    cont = 1
    index = -1
    for i in line[1:-1]:
        if i[:i.find(':')] == codigo:
            index = cont
        cont += 1
    del line[index]
    ls[semestre] = ';'.join(line) 
    
    with open(name_pensum_file,'w') as file:
        file.writelines(ls)
    
    limpiar_superior()
    limpiar_frame_materias()
    actualizar_frame_materias()

def opc_nuevaMateria() -> None:
    if mtNueva.get():
        nmCredLabel.config(height=1, bg=bg_color)
        nmCredText.config(width=4, height=1)
        nmNombLabel.config(height=1, bg=bg_color)
        nmNombText.config(width=60, height=1)
        nmDescLabel.config(height=1, bg=bg_color)
        nmDescText.config(width=60, height=9)
        nmPreLabel.config(width=15, height=1, bg='#A7F69F',font=('Times',12, 'bold'))
        nmPre1Label.config(height=1, bg=bg_color)
        nmPre1Text.config(width=10, height=1)
        nmPreButton.config(width=15, height=2, bg='#F6ECCE', command=x_nm_agregar_prerequisito)
        nmCoLabel.config(width=15, height=1, bg='#A7F69F',font=('Times',12, 'bold'))
        nmCo1Label.config(height=1, bg=bg_color)
        nmCo1Text.config(width=10, height=1)
        nmCoButton.config(width=15, height=2, bg='#F6ECCE', command=x_nm_agregar_corequisito)
            
        nmPreContx.set(810 - 38)
        nmPreConty.set(60)
        nmCoContx.set(810 - 38)
        nmCoConty.set(60 + 100)
        
        nmCredLabel.place(x=182, y=120)
        nmCredText.place(x=190, y=140)
        nmNombLabel.place(x=275, y=225)
        nmNombText.place(x=275, y=245)
        nmDescLabel.place(x=275, y=55)
        nmDescText.place(x=275, y=75)
        nmPreLabel.place(x=910, y=10)
        nmPre1Label.place(x=837, y=5)
        nmPre1Text.place(x=815, y=25)
        nmPreButton.place(x=1070, y=5)
        nmCoLabel.place(x=910, y=10 + 100)
        nmCo1Label.place(x=837, y=5 + 100)
        nmCo1Text.place(x=815, y=25 + 100)
        nmCoButton.place(x=1070, y= 5 + 100)
    else:
        limpiar_nuevaMateria()

def opcionesMateria(codigoMateria: str, semestre: int) -> None:
    found = False
    mts = actualizar_materias()
    for i in mts:
        if i == codigoMateria:
            found = True
            limpiar_superior()
            infAlertLabel.place_forget()
            
            infMainLabel['text'] = codigoMateria
            infCredLabel['text'] = mts[i]['Creditos']
            
            dcp = ''
            for j in range(len(mts[i]['Descripcion'])):
                if len(dcp) != 0 and len(dcp)%165 == 0:
                    if 'a' < mts[i]['Descripcion'][j] < 'z' or 'A' < mts[i]['Descripcion'][j] < 'Z' or '0' < mts[i]['Descripcion'][j] < '9':
                        dcp += '-'
                    dcp += '\n'
                dcp += mts[i]['Descripcion'][j]
            
            infDescLabel['text'] = dcp
            infEstLabel['text'] = mts[i]['Estado']
            
            label = tk.Label(frm, text='Prerequisitos:')
            label.config(width=10, height=1, bg='#7CD6E0')
            infPre.append(label)
            for j in mts[i]['Prerequisitos']:
                if len(j) > 1:
                    label = tk.Label(frm, text='(')
                    label.config(width=1, height=1, bg='#7CD6E0')
                    infPre.append(label)
                    for k in j:
                        button = tk.Button(frm, text=k, command=partial(opcionesMateria,k, 0))
                        button.config(width=8, height= 1, bg=colorMateria(k))
                        infPre.append(button)
                        label = tk.Label(frm, text='O')
                        label.config(width=1, height=1, bg='#7CD6E0')
                        infPre.append(label)
                    del infPre[len(infPre) - 1]
                    label = tk.Label(frm, text=')')
                    label.config(width=1, height=1, bg='#7CD6E0')
                    infPre.append(label)
                else:
                    button = tk.Button(frm, text=j[0], command=partial(opcionesMateria, j[0], 0))
                    button.config(width=8, height=1, bg=colorMateria(j[0]))
                    infPre.append(button)
                label = tk.Label(frm, text='Y')
                label.config(width=1, height=1, bg='#7CD6E0')
                infPre.append(label)
            del infPre[len(infPre) - 1]
            
            label = tk.Label(frm, text='Corequisitos:')
            label.config(width=10, height=1, bg='#7CD6E0')
            infCo.append(label)
            for j in mts[i]['Corequisitos']:
                if len(j) > 1:
                    label = tk.Label(frm, text='(')
                    label.config(width=1, height=1, bg='#7CD6E0')
                    infCo.append(label)
                    for k in j:
                        button = tk.Button(frm, text=k, command=partial(opcionesMateria,k, 0))
                        button.config(width=8, height= 1, bg=colorMateria(k))
                        infCo.append(button)
                        label = tk.Label(frm, text='O')
                        label.config(width=1, height=1, bg='#7CD6E0')
                        infCo.append(label)
                    del infCo[len(infCo) - 1]
                    label = tk.Label(frm, text=')')
                    label.config(width=1, height=1, bg='#7CD6E0')
                    infCo.append(label)
                else:
                    button = tk.Button(frm, text=j[0], command=partial(opcionesMateria, j[0], 0))
                    button.config(width=8, height=1, bg=colorMateria(j[0]))
                    infCo.append(button)
                label = tk.Label(frm, text='Y')
                label.config(width=1, height=1, bg='#7CD6E0')
                infCo.append(label)
            del infCo[len(infCo) - 1]
            infNombLabel['text'] = mts[i]['Nombre']
            if semestre != 0:
                infElimButton['command'] = partial(x_quitar_materia_semestre,codigoMateria,semestre)
                infElimButton.place(x=75, y=225)
            
            
            infMainLabel.config(width=20, height=2, bg = colorMateria(codigoMateria), font=('MS Serif', 12,'bold italic'))
            infCredLabel.config(width=4, height=2, bg = '#88A58D', font=('MS Serif', 12,'bold'))
            infDescLabel.config(width=200, height=9, bg= '#B5D0BA', font=('Times',10), anchor='w')
            infEstLabel.config(width=26, height=1, font=('MS Serif', 10,'bold'))
            infNombLabel.config(height=1, font=('MS Serif', 10, 'bold'), bg=bg_color)            
            
            if mts[i]['Estado'] == 'Aprobado':
                infEstLabel.config(bg= '#3FBB55')
            elif mts[i]['Estado'] == 'Reprobado':
                infEstLabel.config(bg= '#E64444')
            else:
                infEstLabel.config(bg= '#A0C2C6')
            
            QuitButton.place(x= 100, y=90)
            infMainLabel.place(x=25, y=150)
            infCredLabel.place(x=225, y=150)
            infDescLabel.place(x=275,y=70)
            infEstLabel.place(x=28, y=194)
            infNombLabel.place(x=20, y=35)
            
            try:
                infPre[0].place(x=275, y=220 + 3)
            except:
                pass
            contx = 355
            for j in range(len(infPre[1:])):
                if type(infPre[j + 1]) is tk.Label:
                    infPre[j + 1].place(x=contx, y=220 + 3)
                    contx += 12
                else:
                    infPre[j + 1].place(x=contx, y=220)
                    contx += 67
            try:
                infCo[0].place(x=275, y=220 + 3 + 28)
            except:
                pass
            contx = 355
            for j in range(len(infCo[1:])):
                if type(infCo[j + 1]) is tk.Label:
                    infCo[j + 1].place(x=contx, y=220 + 3 + 28)
                    contx += 12
                else:
                    infCo[j + 1].place(x=contx, y=220 + 28)
                    contx += 67
    if not found:
        limpiar_cambiarMateria()
        limpiar_nuevaMateria()
        infAlertLabel['text'] = f'Materia {codigoMateria}\n no está registrada.'
        infAlertLabel.place(x=900, y=20)
        QuitButton.place(x= 100, y=90)

def x_cambiar_dpto(evt) -> None:
    chgMat1Text.delete('1.0',tk.END)
    chgMat1Text.insert(tk.INSERT, evt.widget.get(int(evt.widget.curselection()[0])) )

def x_mostrar_dptos(evt) -> None:        
    if not chgMat1ListB.winfo_ismapped() and len(obtener_dptos(chgMat1Text.get('1.0','end-1c'))) != 0:
        chgMat1ListB.delete(0,tk.END)
        chgMat1ListB.insert(1, *obtener_dptos(chgMat1Text.get('1.0','end-1c')))
        if chgMat1ListB.size() == 0:
            pass
        elif chgMat1ListB.size() <= 3:
            chgMat1ListB.config(width=13,height=chgMat1ListB.size())
        else:
            chgMat1Scrollbar.place(x=157, y=120)
            chgMat1ListB.config(width=13, height=3)
        
        chgMat1ListB.bind('<<ListboxSelect>>',x_cambiar_dpto)
        chgMat1ListB.place(x=75, y=120)
        
def x_quitar_dptos(evt) -> None:
    chgMat1Scrollbar.place_forget()
    chgMat1ListB.place_forget()

def agregarMateria(numSemestre: int) -> None:
    limpiar_superior()
    
    chgMain2Label.config(text=f'Agregar Materia al Semestre {numSemestre}')
    chgMain2Label.place(x=59, y=20)
    
    chgMat1Label.config(height=1, bg=bg_color)
    chgMat1Label.place(x=76, y=80)
    
    chgMat1Text.config(width=10,height=1)
    chgMat1Text.insert(tk.END, '')
    chgMat1Text.place(x=75,y=100)
    chgMat1Text.bind('<FocusIn>',x_mostrar_dptos)
    chgMat1Text.bind('<FocusOut>',x_quitar_dptos)
    
    chgMat2Label.config(height=1, bg=bg_color)
    chgMat2Label.place(x=185, y=80)
    
    chgMat2Text.config(width=10,height=1)
    chgMat2Text.insert(tk.END, '')
    chgMat2Text.place(x=170,y=100)
    
    chgAskCheck.config(width=10, height=1, bg=bg_color)
    chgAskCheck.place(x=110, y=175)
    
    chgButton.config(width=15, height=2, bg='#83E353', font=('MS Serif', 12, 'bold'))
    chgButton['text'] = f'Agregar Materia al\nsemestre {numSemestre}'
    chgButton['command'] = partial(agregarMateria_module, numSemestre)
    chgButton.place(x=910, y=200)
    
    chgMat1Scrollbar.config(command=chgMat1ListB.yview)
    chgMat1ListB.config(yscrollcommand=chgMat1Scrollbar.set)
    
    QuitButton.place(x=100, y= 210)

def colorMateria(codigoMateria: str) -> str:
    #if 'ISIS' in codigoMateria:
    if any(i in codigoMateria for i in ['ISIS', 'MISW', 'MISO', 'MINE', 'MESI']):
        return '#3CDFD5'
    elif 'IELE' in codigoMateria:
        return '#DDD539'
    elif 'LENG' in codigoMateria:
        return '#E187E2'
    elif 'MATE' in codigoMateria:
        return '#EF1010'
    elif 'FISI' in codigoMateria or 'QUIM' in codigoMateria or 'IIND' in codigoMateria:
        return '#B0545F'
    elif 'CB' in codigoMateria:
        return '#9A62E3'
    else:
        return '#91EE89'

def actualizar_frame_materias() -> None:
    data = actualizar_pensum()
    
    widget_mts.clear()
    
    #Poner en el Frame las materias y su información.
    semcont = 0         
    contx = 0
    conty = frm_height - 400
    credcont = 0
    totcredcont = 0
    totmatcont = 0
    
    for i in data:
        credcont = 0
        conty = frm_height - 400
        contx += 100
        semcont += 1
        totmatcont += len(i)
        
        semLabel = tk.Label(frm, text=semcont)
        semLabel.config(width=12, height=1, bg='#125281', fg='#C4D4DF', font=('Times',10,'bold'))
        semLabel.place(x=contx, y=conty - 2)
        if len(i) < 13:
            agrButton = tk.Button(frm, text='+',command=partial(agregarMateria,semcont))
            agrButton.config(width=3, height=1)
            agrButton.place(x=contx, y=conty - 4)
        
        for j in range(len(i)):
            credcont += i[j][1]
            conty += 25
            
            button = tk.Button(frm, text=i[j][0], command=partial(opcionesMateria, i[j][0], semcont) )
            button.config(width=10, height= 1, bg = colorMateria(i[j][0]))
            label = tk.Label(frm, text=i[j][1])
            label.config(width=2, height= 1, bg = colorMateria(i[j][0]))
            
            
            widget_mts[i[j][0]] = (button, label)
            
            
            button.place(x=contx, y=conty)
            label.place(x=contx + 80, y=conty + 2)
        totcredcont += credcont
        
        numMatLabel = tk.Label(frm, text=f'{len(i)} materias')
        numMatLabel.config(width=12, height= 1)
        if len(i) >= 12:
            numMatLabel.config(bg='#DF1E41')
        elif len(i) >= 10:
            numMatLabel.config(bg='#E6C55D')
        else:
            numMatLabel.config(bg='#F7D7D7')
        numMatLabel.place(x=contx, y=frm_height - 50)
        numCredLabel = tk.Label(frm, text=f'{credcont} créditos')
        numCredLabel.config(width=12, height= 1)
        if credcont > 25:
            numCredLabel.config(bg='#DF1E41')
        elif credcont >= 20:
            numCredLabel.config(bg='#E6C55D')
        else:
            numCredLabel.config(bg='#F7D7D7')
        numCredLabel.place(x=contx, y= frm_height - 25)
    
    infLabel = tk.Label(frm, text='Totales')
    infLabel.config(width=12, height=1, bg='#125281', fg='#C4D4DF', font=('Times',10,'bold'))
    infLabel.place(x=contx + 100, y=605)
    
    totalLabel = tk.Label(frm, text=f'{totmatcont} Materias')
    totalLabel.config(width=12, height=1, bg='#000000', fg='#ffffff')
    totalLabel.place(x=contx + 100, y=630)
    
    totalLabel = tk.Label(frm, text=f'{totcredcont} Créditos')
    totalLabel.config(width=12, height=1, bg='#000000', fg='#ffffff')
    totalLabel.place(x=contx + 100, y=655)
    
def limpiar_frame_materias() -> None:
    for i in widget_mts:
        widget_mts[i][0].place_forget()
        widget_mts[i][1].place_forget()

def actualizar_materias() -> dict:
    with open(name_courses_file,'r') as file:
        lines=file.readlines()[1:]
        mts = {}
        for i in lines:
            i = i.split(';')
            mts[i[0]] = {}
            mts[i[0]]['Nombre'] = i[1]
            mts[i[0]]['Creditos'] = i[2]
            mts[i[0]]['Estado'] = i[5]
            mts[i[0]]['Descripcion'] = i[6]
            mts[i[0]]['Prerequisitos'] = ()
            if i[3] != '':
                for j in i[3].split(':'):
                    j = j.split('?')
                    mts[i[0]]['Prerequisitos'] += (tuple(j),)
            mts[i[0]]['Corequisitos'] = ()
            if i[4] != '':
                for j in i[4].split(':'):
                    j = j.split('?')
                    mts[i[0]]['Corequisitos'] += (tuple(j),)
    return mts

def actualizar_pensum() -> list:
    with open(name_pensum_file, 'r') as file:
        lines = file.readlines()[1:]
        data = []
        for i in range(len(lines)):
            data.append([])
        for i in lines:
            for j in i.rstrip().split(';')[1:-1]:
                try:
                    data[int(i.split(';')[0]) - 1].append((j.split(':')[0],int(j.split(':')[1])))
                except IndexError:
                    pass
    return data 

def limpiar_superior() -> None:
    limpiar_cambiarMateria()
    limpiar_infoMateria()
    limpiar_nuevaMateria()

def limpiar_cambiarMateria() -> None:
    chgMain2Label.place_forget()
    chgMat1Label.place_forget()
    chgMat1Text.place_forget()
    chgMat1Text.delete('1.0', tk.END)
    chgMat1Scrollbar.place_forget()
    chgMat1ListB.place_forget()
    chgMat2Label.place_forget()
    chgMat2Text.delete('1.0', tk.END)
    chgMat2Text.place_forget()
    chgAlertLabel.place_forget()
    chgAskCheck.deselect()
    chgAskCheck.place_forget()
    chgButton.place_forget()
    QuitButton.place_forget()

def limpiar_infoMateria() -> None:
    infAlertLabel.place_forget()
    QuitButton.place_forget()
    infElimButton.place_forget()
    infMainLabel.place_forget()
    infNombLabel.place_forget()
    infCredLabel.place_forget()
    infDescLabel.place_forget()
    infEstLabel.place_forget()
    for i in infPre:
        i.place_forget()
    for i in infCo:
        i.place_forget()
    infPre.clear()
    infCo.clear()

def limpiar_nuevaMateria() -> None:
    nmCredLabel.place_forget()
    nmCredText.delete('1.0',tk.END)
    nmCredText.place_forget()
    nmNombLabel.place_forget()
    nmNombText.delete('1.0',tk.END)
    nmNombText.place_forget()
    nmDescLabel.place_forget()
    nmDescText.delete('1.0',tk.END)
    nmDescText.place_forget()
    nmPreLabel.place_forget()
    nmPre1Label.place_forget()
    nmPre1Text.delete('1.0',tk.END)
    nmPre1Text.place_forget()
    nmPreButton.place_forget()
    nmCoLabel.place_forget()
    nmCo1Label.place_forget()
    nmCo1Text.delete('1.0',tk.END)
    nmCo1Text.place_forget()
    nmCoButton.place_forget()
    for i in nmPre:
        i.place_forget()
    nmPre.clear()
    for i in nmCo:
        i.place_forget()
    nmCo.clear()
    
#MAIN APP

try:
    with open(name_pensum_file,'r') as file:
        # change numSems for the number of lines - 1 (the first line is the header)
        numSems = len(file.readlines())-1 # fix the number of semesters to be the number of lines in the file and not just 10
        print(numSems)

except FileNotFoundError:
    with open(name_pensum_file,'w') as file:
        file.write('Semestre;Código Materia:Créditos;Estado')
        for i in range(numSems):
            file.write(f'\n{i+1};;Pendiente')
        file.close()

try:
    open(name_courses_file,'r')
except FileNotFoundError:
    with open(name_courses_file,'w') as file:
        file.write('Código Materia;Nombre;Créditos;Prerequisitos(?:)*;Corequisitos(?:)*;Estado;Descripción')
        file.close()

# width and height of the frame        
frm_width = min(max(100*(numSems+2),1200),1600) # min 1200, max 1600
frm_height = 680

mts = {}
mts = actualizar_materias()
data = []
data = actualizar_pensum()

#Configuración Inicial del Frame.
root = tk.Tk()
root.title('PensuManager')
try:
    root.iconbitmap('pensumanager.ico')
except:
    pass
root.resizable(width=False, height=False)
frm = tk.Frame(root)
frm.config(width=frm_width, height=frm_height, bg=bg_color)    
frm.pack()

titleLabel = tk.Label(frm, text='PensuManager')
titleLabel.config(bg='#ABD4CA', fg= '#1E3049', font=('MS Serif',20))
titleLabel.place(x=500,y=20)

#Widgets de información (ocultos).
QuitButton = tk.Button(frm, text='Quitar Selección', command=limpiar_superior)
QuitButton.config(width=15,height=1, bg='#977638')
                  
infElimButton = tk.Button(frm, text='Eliminar\ndel Semestre')
infElimButton.config(width=15, height=2, bg='#FC4B4B')

infAlertLabel = tk.Label(frm)
infAlertLabel.config(width=30, height=2, fg='#E14A4A', bg='#B9B3B3', font=('Times',12, 'bold'))
infMainLabel = tk.Label(frm)
infNombLabel = tk.Label(frm)
infCredLabel = tk.Label(frm)
infDescLabel = tk.Label(frm)
infEstLabel = tk.Label(frm)
infPre = []
infCo = [] 

#Widgets de agregar o cambiar (ocultos).
mtNueva = tk.BooleanVar(frm)

chgMain2Label = tk.Label(frm, width=30, height=1, bg='#7DE573', font=('Times', 10, 'bold'))
chgMat1Label = tk.Label(frm, text='Departamento')
chgMat1Text = tk.Text(frm)
chgMat1Scrollbar = tk.Scrollbar(frm)
chgMat1ListB = tk.Listbox(frm)
chgMat2Label = tk.Label(frm, text='Número')
chgMat2Text = tk.Text(frm)
chgAlertLabel = tk.Label(frm)
chgAlertLabel.config(fg='#E14A4A', bg='#B9B3B3', font=('Times',12, 'bold'))
chgAskCheck = tk.Checkbutton(frm, text='Materia Nueva', command=opc_nuevaMateria, variable=mtNueva, onvalue=True, offvalue=False)
chgButton = tk.Button(frm)

#Widgets nueva materia (ocultos).
nmPre = []
nmCo = []
nmPreContx = tk.IntVar(frm)
nmPreConty = tk.IntVar(frm)
nmCoContx = tk.IntVar(frm)
nmCoConty = tk.IntVar(frm)

nmCredLabel = tk.Label(frm, text= 'Créditos')
nmCredText = tk.Text(frm)
nmNombLabel = tk.Label(frm, text='Nombre Materia')
nmNombText = tk.Text(frm)
nmDescLabel = tk.Label(frm, text='Descripción')
nmDescText = tk.Text(frm)
nmPreLabel = tk.Label(frm, text='Prerequisitos')
nmPre1Label = tk.Label(frm, text='Código')
nmPre1Text = tk.Text(frm)
nmPreButton = tk.Button(frm, text='Agregar\n Prerequisito')
nmCoLabel = tk.Label(frm, text='Corequisitos')
nmCo1Label = tk.Label(frm, text='Código')
nmCo1Text = tk.Text(frm)
nmCoButton = tk.Button(frm, text='Agregar\n Corequisito')

'registrada'
#Poner Labels indicativos.
txts = ['Semestre','Materia 1', 'Materia 2', 'Materia 3', 'Materia 4', 'Materia 5',
        'Materia 6', 'Materia 7', 'Materia 8', 'Materia 9', 'Materia 10', 'Materia 11',
        'Materia 12', 'Materia 13', 'Total Materias', 'Total Créditos']
conty = frm_height - 425
for i in txts:
    conty += 25
    infLabel = tk.Label(frm, text=i)
    infLabel.config(width=12, height=1, bg='#125281', fg='#C4D4DF', font=('Times',8,'bold'))
    infLabel.place(x=5, y=conty)
del txts

widget_mts = {}
actualizar_frame_materias()

root.mainloop()
import os
import cv2
import numpy as np
from datetime import datetime
import tflite_runtime.interpreter as tf

#Funciones para estadisticas
def txtPorcentaje(emocion,cantidad, porcentaje):
    # dd_mm_YY___h_m_s
    now = datetime.now()
    array = []
    array = [str(emocion),str(cantidad), 'Porcentaje = ',str(porcentaje)]
    with open(Estadisticas, 'a') as f:
        f.write(' '.join(array))
        f.write('\n')

def txtTotal(emocion, dt_string):
    # dd_mm_YY___h_m_s
    now = datetime.now()
    Emociones_time= now.strftime("%H_%M_%S ")
    array = []
    array = [Emociones_time,emocion]
    with open(Emociones, 'a') as f:
        f.write(' '.join(array))
        f.write('\n')

def printporcentajes(emociones):
    print('-----------------------------------------------')
    print('Estadistica de las emociones detectadas: \n \n')
    directorio = {i:emociones.count(i) for i in emociones}
    suma_emociones = sum(list(directorio.values()))
    for i in list(directorio.keys()):
        print (i, directorio.get(i), 'Porcentaje = ', 100*(directorio.get(i) /suma_emociones))
        txtPorcentaje(i, directorio.get(i), 100*(directorio.get(i) /suma_emociones))
    print('----------------------------------------------- \n')

################################################################################
################################################################################
################################################################################

# GUARDA EL FRAME 

def save_image(emotion_label, frame):
    now = datetime.now()
    
    if not os.path.exists('Emot'):
        os.mkdir('Emot')
        
        
    # Formato de hora: hh_mm_ss
    hour_format = now.strftime("%H_%M_%S")
    # Nombre de archivo de la imagen
    file_name = hour_format + "_" + emotion_label + ".png"
    
    img_path = os.path.join('Emot', file_name)
    # Guardar la imagen
    cv2.imwrite(img_path, frame)
    
################################################################################
################################################################################
################################################################################




################################################################################
face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the TFLite model and allocate tensors.
emotion_interpreter = tf.Interpreter(model_path="5cat_emotion_detection_model_100epochs_no_opt.tflite")
emotion_interpreter.allocate_tensors()

# Get input and output tensors.
emotion_input_details = emotion_interpreter.get_input_details()
emotion_output_details = emotion_interpreter.get_output_details()

# Test the model on input data.
emotion_input_shape = emotion_input_details[0]['shape']

class_labels=['Angry', 'Happy','Neutral','Sad','Surprise']

cap=cv2.VideoCapture(0)
emociones = []
now = datetime.now()
Estadisticas = 'Stat_'+ now.strftime("%H_%M_%S__%d_%m_%Y")+'.txt'
Emociones = 'Total_'+ now.strftime("%H_%M_%S__%d_%m_%Y")+'.txt'
while True:
    ret,frame=cap.read()
    labels=[]

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_classifier.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray=gray[y:y+h,x:x+w]
        roi_gray=cv2.resize(roi_gray,(48,48))/255

        roi= np.array(roi_gray, dtype=np.float32).reshape(-1,48,48,1)

        emotion_interpreter.set_tensor(emotion_input_details[0]['index'], roi)
        emotion_interpreter.invoke()
        emotion_preds = emotion_interpreter.get_tensor(emotion_output_details[0]['index'])

        emotion_label=class_labels[emotion_preds.argmax()]  #Find the label
        emotion_label_position=(x,y)


        cv2.putText(frame,emotion_label,emotion_label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)


        print(emotion_label)
        emociones.append(emotion_label)
        txtTotal(emotion_label,Emociones)
        save_image(emotion_label, frame)



    cv2.imshow('Emotion Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  #Press q to exit
        break
printporcentajes(emociones)
cap.release()
cv2.destroyAllWindows()

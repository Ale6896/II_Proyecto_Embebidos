#SUMMARY = "EMOTION DETECTOR"
#DESCRIPTION = "EMOTION"
#HOMEPAGE = ""
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI = "file://emotion.py \
           file://haarcascade_frontalface_default.xml \
           file://5cat_emotion_detection_model_100epochs_no_opt.tflite "

S = "${WORKDIR}"

TARGET_CC_ARCH += "${LDFLAGS}"

MY_DESTINATION = "/home/root/PROYECTO"

do_install () {
   install -d ${D}${MY_DESTINATION}
   install -m 0755 emotion.py ${D}${MY_DESTINATION}
   
}

do_install_append () {
   install -d ${D}${MY_DESTINATION}
   install -m 0755 haarcascade_frontalface_default.xml ${D}${MY_DESTINATION}
   install -m 0755 5cat_emotion_detection_model_100epochs_no_opt.tflite ${D}${MY_DESTINATION}
}

FILES_${PN} += "/home/root/PROYECTO/emotion.py \
                /home/root/PROYECTO/haarcascade_frontalface_default.xml \
                /home/root/PROYECTO/5cat_emotion_detection_model_100epochs_no_opt.tflite"

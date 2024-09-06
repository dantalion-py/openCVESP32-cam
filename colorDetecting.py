import cv2
import urllib.request
import numpy as np

def nothing(x):
    pass

url = 'http://192.168.211.237/cam-lo.jpg'
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
# Rango HSV para el color azul (con ajuste de sensibilidad)
l_h_b, l_s_b, l_v_b = 90, 50, 50
u_h_b, u_s_b, u_v_b = 145, 255, 255

# Rango HSV para el color rojo (el rojo se define en dos rangos en HSV, ajustado)
l_h_r1, l_s_r1, l_v_r1 = 0, 100, 50
u_h_r1, u_s_r1, u_v_r1 = 10, 255, 255

l_h_r2, l_s_r2, l_v_r2 = 170, 100, 50
u_h_r2, u_s_r2, u_v_r2 = 180, 255, 255

# Rango HSV para el color verde (ajustado)
l_h_g, l_s_g, l_v_g = 30, 40, 50
u_h_g, u_s_g, u_v_g = 90, 255, 255
while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Máscara para el color azul
    l_b = np.array([l_h_b, l_s_b, l_v_b])
    u_b = np.array([u_h_b, u_s_b, u_v_b])
    mask_blue = cv2.inRange(hsv, l_b, u_b)

    # Máscara para el color rojo (combina dos rangos)
    l_r1 = np.array([l_h_r1, l_s_r1, l_v_r1])
    u_r1 = np.array([u_h_r1, u_s_r1, u_v_r1])
    mask_red1 = cv2.inRange(hsv, l_r1, u_r1)

    l_r2 = np.array([l_h_r2, l_s_r2, l_v_r2])
    u_r2 = np.array([u_h_r2, u_s_r2, u_v_r2])
    mask_red2 = cv2.inRange(hsv, l_r2, u_r2)

    mask_red = cv2.add(mask_red1, mask_red2)

    # Máscara para el color verde
    l_g = np.array([l_h_g, l_s_g, l_v_g])
    u_g = np.array([u_h_g, u_s_g, u_v_g])
    mask_green = cv2.inRange(hsv, l_g, u_g)

    def draw_rectangles(mask, frame, color_name, color_bgr):
        cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        found = False  # Variable para indicar si se encontró un contorno
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 2000:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 3)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.putText(frame, color_name, (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, color_bgr, 2)
                found = True  # Se encontró un contorno
        return found  # Retornar True si se encontró un contorno

    # Dibujar cuadrados para azul, rojo y verde
    blue_a = draw_rectangles(mask_blue, frame, "blue", (255, 0, 0))
    red_a = draw_rectangles(mask_red, frame, "red", (0, 0, 255))
    green_a = draw_rectangles(mask_green, frame, "green", (0, 255, 0)) 
    if blue_a:
        print("go to blue")
    elif red_a:
        print("go to red")
    elif green_a:
        print("go to green")
    else:
        print("none")


    # Muestra el resultado
    cv2.imshow("live transmission", frame)
    key = cv2.waitKey(5)
    if key == ord('a'):
        break

cv2.destroyAllWindows()

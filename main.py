def Zeitmessung(Dauer: number):
    global ZeitUnbewegt, boAlarm, boReset, boBewegungRegistriert
    if boStarteMessung == 1:
        basic.pause(1000)
        ZeitUnbewegt += 1
        if 60 * Dauer <= ZeitUnbewegt:
            boAlarm = 1
        if boReset > 0 or boBewegungRegistriert > 0:
            boAlarm = 0
            ZeitUnbewegt = 0
            boReset = 0
            boBewegungRegistriert = 0
def BewegungErkennen():
    global boBewegungRegistriert, ZählerBewegungX, Last_x
    # Neuer Block (ArrayListe) wird ausgewertet
    if zeiger_Arrays == 1:
        basic.set_led_color(0xff00ff)
        boBewegungRegistriert = 0
        ZählerBewegungX = 0
    # Wurde eine Bewegung festgestellt?
    if abs(Mittelwert_X - Last_x) > SchwellwertBewegung:
        ZählerBewegungX += 1
        serial.write_value("Zähler+", ZählerBewegungX)
    if ZählerBewegungX > HäufigkeitBewegungsErkannt:
        boBewegungRegistriert = 1
        basic.set_led_color(0x00ff00)
    Last_x = Mittelwert_X
# Fehlerquellen:
# 
# Erschütterungen (Zugfahrt)
# 
# Calliope fällt runter
# 
# Calliope wird zur Seite gelegt und nicht bewegt.
def MesseBeschleunigungXYZSt():
    global Mittelwert_X, Mittelwert_Y, Mittelwert_Z, Mittelwert_Stärke, zeiger_Arrays, boArrayVoll, boToggle
    for index in range(20):
        Mittelwert_X = (input.acceleration(Dimension.X) + 19 * Mittelwert_X) / 20
        Mittelwert_Y = (input.acceleration(Dimension.Y) + 19 * Mittelwert_Y) / 20
        Mittelwert_Z = (input.acceleration(Dimension.Z) + 19 * Mittelwert_Z) / 20
        Mittelwert_Stärke = (input.acceleration(Dimension.STRENGTH) + 19 * Mittelwert_Stärke) / 20
        basic.pause(50)
    if len(WertelisteX) < ArrayGröße:
        WertelisteX.append(Mittelwert_X)
        WertelisteY.append(Mittelwert_Y)
        WertelisteZ.append(Mittelwert_Z)
        WertelisteStärke.append(Mittelwert_Stärke)
        zeiger_Arrays = zeiger_Arrays + 1
    else:
        if boArrayVoll == 0:
            music.play_tone(262, music.beat(BeatFraction.WHOLE))
            boArrayVoll = 1
        if zeiger_Arrays >= ArrayGröße:
            zeiger_Arrays = 0
        else:
            zeiger_Arrays = zeiger_Arrays + 1
        WertelisteX[zeiger_Arrays] = Mittelwert_X
        WertelisteY[zeiger_Arrays] = Mittelwert_Y
        WertelisteZ[zeiger_Arrays] = Mittelwert_Z
        WertelisteStärke[zeiger_Arrays] = Mittelwert_Stärke
    boToggle = 1 - boToggle
    serial.write_value("x", Mittelwert_X)
    serial.write_value("Zeigerarry", zeiger_Arrays)
    BewegungErkennen()
    return 0
# Programmablauf:
# 
# Zu Beginn: Warten 100ms? Danach Bewegungsmesser starten
# 
# Zeit starten, in der Bewegungsregistration stattfindet.
# 
# Wenn keine Bewegung erkannt wurde (innerhalb der Zeit), dann Ausgabe
# 
# Reset der Ausgabe, wenn wieder Bewegung registriert wurde oder manueller Reset

def on_button_pressed_a():
    global boStarteMessung, boReset
    boStarteMessung = 1
    boReset = 1
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global boStarteMessung, boTransfer, Zeiger_Senden, Index
    boStarteMessung = 0
    boTransfer = 1
    Zeiger_Senden = zeiger_Arrays
    serial.write_line("Ausgabe")
    Index = 0
    while Index <= len(WertelisteX) - 1:
        led.toggle(5, 5)
        serial.write_number(WertelisteX[Zeiger_Senden])
        serial.write_string(";")
        serial.write_number(WertelisteY[Zeiger_Senden])
        serial.write_string(";")
        serial.write_number(WertelisteZ[Zeiger_Senden])
        serial.write_string(";")
        serial.write_number(WertelisteStärke[Zeiger_Senden])
        serial.write_line("")
        Index += 1
        Zeiger_Senden += 1
        if Zeiger_Senden >= len(WertelisteX):
            Zeiger_Senden = 0
    music.play_tone(349, music.beat(BeatFraction.DOUBLE))
    boTransfer = 0
input.on_button_pressed(Button.B, on_button_pressed_b)

Index = 0
Zeiger_Senden = 0
boTransfer = 0
boToggle = 0
WertelisteStärke: List[number] = []
WertelisteZ: List[number] = []
WertelisteY: List[number] = []
WertelisteX: List[number] = []
Mittelwert_Stärke = 0
Mittelwert_Z = 0
Mittelwert_Y = 0
Last_x = 0
Mittelwert_X = 0
ZählerBewegungX = 0
boBewegungRegistriert = 0
boReset = 0
ZeitUnbewegt = 0
boStarteMessung = 0
SchwellwertBewegung = 0
HäufigkeitBewegungsErkannt = 0
zeiger_Arrays = 0
ArrayGröße = 0
boArrayVoll = 0
boAlarm = 0
def AlarmAusgeben(Alarm: any, Akustisch: bool, Optisch: bool):
    if Alarm:
        if Akustisch:
            music.play_melody("C E C E C E ", 120)
    if Optisch:
        basic.set_led_color(0xff0000)
        basic.pause(200)
        basic.set_led_color(0x0000ff)
        basic.pause(200)
    else:
        basic.set_led_color(0x000000)
boArrayVoll = 0
serial.set_baud_rate(BaudRate.BAUD_RATE115200)
ArrayGröße = 10
zeiger_Arrays = 0
# Dauer in Minuten
ZeitMaxUnbeweglichkeit = 1
# Dauer in Minuten
HäufigkeitBewegungsErkannt = 5
SchwellwertBewegung = 100
# Fragen an Messungen:
# 
# Wie sieht die Bewegung aus, wenn man steht? --> Messwertaufnahme und Auswertung

def on_forever():
    # Dauer in Minuten
    Zeitmessung(ZeitMaxUnbeweglichkeit)
    AlarmAusgeben(boAlarm >= 1, True, True)
    if boStarteMessung == 1:
        MesseBeschleunigungXYZSt()
        if boToggle:
            basic.show_icon(IconNames.HEART)
        else:
            basic.show_icon(IconNames.SMALL_HEART)
    elif boTransfer == 1:
        basic.show_icon(IconNames.ARROW_EAST)
    else:
        basic.show_icon(IconNames.YES)
basic.forever(on_forever)

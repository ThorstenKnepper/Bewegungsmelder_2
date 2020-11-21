"""

Wie wird Bewegung registriert?

Alle Richtungen haben einen maximal, minimal und Durchschnittswert über eine Zeitdauer.

Wenn die Pegel (von min bis max) innerhalb der Zeitdauer einen Grenzwert überschreiten und die Anzahl dieser Überschreitungen einen Grenzwert "Häufigkeit" überschreitet: Dann liegt Bewegung vor

Zeitraum: 20 Sekunden

Häufigkeit: 5 Mal

Grenzwert: 100

"""
"""

Programmablauf:

    Zu Beginn: Warten 100ms? Danach Bewegungsmesser starten

Zeit starten, in der Bewegungsregistration stattfindet.

Wenn keine Bewegung erkannt wurde (innerhalb der Zeit), dann Ausgabe

Reset der Ausgabe, wenn wieder Bewegung registriert wurde oder manueller Reset

"""
"""

Bewegung registrieren

Wenn Bewegung, dann Variable BEWEGUNG setzen: TRUE

Wenn keine Bewegung, dann Variable Bewegung: FALSCH

Grenzwert definieren: Wenn Grenzwert überschritten, dann Bewegung erkannt.

Lage erfassen: Wenn horizontale Position, dann nicht aktiv.

Dauer der Bewegung festlegen, bis es als Bewegung angesehen wird

"""
"""

Fragen an Messungen:

    Wie sieht die Bewegung aus, wenn man steht? --> Messwertaufnahme und Auswertung

"""
def Zeitmessung(Dauer: number):
    global ZeitUnbewegt, boAlarm, boReset
    boBewegungRegistriert = 0
    basic.pause(1000)
    ZeitUnbewegt += 1
    if 60 * Dauer <= ZeitUnbewegt:
        boAlarm = 1
    if boReset > 0 or boBewegungRegistriert > 0:
        boAlarm = 0
        ZeitUnbewegt = 0
        boReset = 0
def AlarmAusgeben(Alarm: bool, Akustisch: bool, Optisch: bool):
    if Alarm:
        if Akustisch:
            music.play_melody("C E C E C E C C ", 120)
        if Optisch:
            basic.set_led_color(0xff0000)
            basic.pause(200)
            basic.set_led_color(0x0000ff)
            basic.pause(200)
    else:
        basic.set_led_color(0x000000)
def BewegungErkennen():
    pass
# Fehlerquellen:
    #
# Erschütterungen (Zugfahrt)
# 
# Calliope fällt runter
# 
# Calliope wird zur Seite gelegt und nicht bewegt.
def MesseBeschleunigungXYZSt():
    global zeiger_Arrays, Mittelwert_X, Mittelwert_Y, Mittelwert_Z, Mittelwert_Stärke, boArrayVoll, boToggle
    zeiger_Arrays = 0
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
    led.toggle(0, 0)
    boToggle = 1 - boToggle

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
boStarteMessung = 0
boToggle = 0
WertelisteStärke: List[number] = []
WertelisteZ: List[number] = []
WertelisteY: List[number] = []
WertelisteX: List[number] = []
Mittelwert_Stärke = 0
Mittelwert_Z = 0
Mittelwert_Y = 0
Mittelwert_X = 0
zeiger_Arrays = 0
boReset = 0
boAlarm = 0
ZeitUnbewegt = 0
ArrayGröße = 0
boArrayVoll = 0
boArrayVoll = 0
serial.set_baud_rate(BaudRate.BAUD_RATE115200)
ArrayGröße = 60
# Dauer in Minuten
ZeitMaxUnbeweglichkeit = 30
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


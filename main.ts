/** 

Wie wird Bewegung registriert?

Alle Richtungen haben einen maximal, minimal und Durchschnittswert über eine Zeitdauer.

Wenn die Pegel (von min bis max) innerhalb der Zeitdauer einen Grenzwert überschreiten und die Anzahl dieser Überschreitungen einen Grenzwert "Häufigkeit" überschreitet: Dann liegt Bewegung vor

Zeitraum: 20 Sekunden

Häufigkeit: 5 Mal

Grenzwert: 100


 */
/** 

Programmablauf:

    Zu Beginn: Warten 100ms? Danach Bewegungsmesser starten

Zeit starten, in der Bewegungsregistration stattfindet.

Wenn keine Bewegung erkannt wurde (innerhalb der Zeit), dann Ausgabe

Reset der Ausgabe, wenn wieder Bewegung registriert wurde oder manueller Reset


 */
/** 

Bewegung registrieren

Wenn Bewegung, dann Variable BEWEGUNG setzen: TRUE

Wenn keine Bewegung, dann Variable Bewegung: FALSCH

Grenzwert definieren: Wenn Grenzwert überschritten, dann Bewegung erkannt.

Lage erfassen: Wenn horizontale Position, dann nicht aktiv.

Dauer der Bewegung festlegen, bis es als Bewegung angesehen wird


 */
/** 

Fragen an Messungen:

    Wie sieht die Bewegung aus, wenn man steht? --> Messwertaufnahme und Auswertung


 */
function Zeitmessung(Dauer: number) {
    
    let boBewegungRegistriert = 0
    basic.pause(1000)
    ZeitUnbewegt += 1
    if (60 * Dauer <= ZeitUnbewegt) {
        boAlarm = 1
    }
    
    if (boReset > 0 || boBewegungRegistriert > 0) {
        boAlarm = 0
        ZeitUnbewegt = 0
        boReset = 0
    }
    
}

function AlarmAusgeben(Alarm: any, Akustisch: boolean, Optisch: boolean) {
    if (Alarm) {
        if (Akustisch) {
            music.playMelody("C E C E C E C C ", 120)
        }
        
        if (Optisch) {
            basic.setLedColor(0xff0000)
            basic.pause(200)
            basic.setLedColor(0x0000ff)
            basic.pause(200)
        }
        
    } else {
        basic.setLedColor(0x000000)
    }
    
}

function BewegungErkennen() {
    
}

//  Fehlerquellen:
// 
//  Erschütterungen (Zugfahrt)
//  
//  Calliope fällt runter
//  
//  Calliope wird zur Seite gelegt und nicht bewegt.
function MesseBeschleunigungXYZSt() {
    
    zeiger_Arrays = 0
    for (let index = 0; index < 20; index++) {
        Mittelwert_X = (input.acceleration(Dimension.X) + 19 * Mittelwert_X) / 20
        Mittelwert_Y = (input.acceleration(Dimension.Y) + 19 * Mittelwert_Y) / 20
        Mittelwert_Z = (input.acceleration(Dimension.Z) + 19 * Mittelwert_Z) / 20
        Mittelwert_Stärke = (input.acceleration(Dimension.Strength) + 19 * Mittelwert_Stärke) / 20
        basic.pause(50)
    }
    if (WertelisteX.length < ArrayGröße) {
        WertelisteX.push(Mittelwert_X)
        WertelisteY.push(Mittelwert_Y)
        WertelisteZ.push(Mittelwert_Z)
        WertelisteStärke.push(Mittelwert_Stärke)
        zeiger_Arrays = zeiger_Arrays + 1
    } else {
        if (boArrayVoll == 0) {
            music.playTone(262, music.beat(BeatFraction.Whole))
            boArrayVoll = 1
        }
        
        if (zeiger_Arrays >= ArrayGröße) {
            zeiger_Arrays = 0
        } else {
            zeiger_Arrays = zeiger_Arrays + 1
        }
        
        WertelisteX[zeiger_Arrays] = Mittelwert_X
        WertelisteY[zeiger_Arrays] = Mittelwert_Y
        WertelisteZ[zeiger_Arrays] = Mittelwert_Z
        WertelisteStärke[zeiger_Arrays] = Mittelwert_Stärke
    }
    
    led.toggle(0, 0)
    boToggle = 1 - boToggle
}

input.onButtonPressed(Button.A, function on_button_pressed_a() {
    
    boStarteMessung = 1
    boReset = 1
})
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    
    boStarteMessung = 0
    boTransfer = 1
    Zeiger_Senden = zeiger_Arrays
    serial.writeLine("Ausgabe")
    Index = 0
    while (Index <= WertelisteX.length - 1) {
        led.toggle(5, 5)
        serial.writeNumber(WertelisteX[Zeiger_Senden])
        serial.writeString(";")
        serial.writeNumber(WertelisteY[Zeiger_Senden])
        serial.writeString(";")
        serial.writeNumber(WertelisteZ[Zeiger_Senden])
        serial.writeString(";")
        serial.writeNumber(WertelisteStärke[Zeiger_Senden])
        serial.writeLine("")
        Index += 1
        Zeiger_Senden += 1
        if (Zeiger_Senden >= WertelisteX.length) {
            Zeiger_Senden = 0
        }
        
    }
    music.playTone(349, music.beat(BeatFraction.Double))
    boTransfer = 0
})
let Index = 0
let Zeiger_Senden = 0
let boTransfer = 0
let boStarteMessung = 0
let boToggle = 0
let WertelisteStärke : number[] = []
let WertelisteZ : number[] = []
let WertelisteY : number[] = []
let WertelisteX : number[] = []
let Mittelwert_Stärke = 0
let Mittelwert_Z = 0
let Mittelwert_Y = 0
let Mittelwert_X = 0
let zeiger_Arrays = 0
let boReset = 0
let boAlarm = 0
let ZeitUnbewegt = 0
let ArrayGröße = 0
let boArrayVoll = 0
boArrayVoll = 0
serial.setBaudRate(BaudRate.BaudRate115200)
ArrayGröße = 60
//  Dauer in Minuten
let ZeitMaxUnbeweglichkeit = 30
//  Fragen an Messungen:
// 
//  Wie sieht die Bewegung aus, wenn man steht? --> Messwertaufnahme und Auswertung
basic.forever(function on_forever() {
    //  Dauer in Minuten
    Zeitmessung(ZeitMaxUnbeweglichkeit)
    AlarmAusgeben(boAlarm >= 1, true, true)
    if (boStarteMessung == 1) {
        MesseBeschleunigungXYZSt()
        if (boToggle) {
            basic.showIcon(IconNames.Heart)
        } else {
            basic.showIcon(IconNames.SmallHeart)
        }
        
    } else if (boTransfer == 1) {
        basic.showIcon(IconNames.ArrowEast)
    } else {
        basic.showIcon(IconNames.Yes)
    }
    
})

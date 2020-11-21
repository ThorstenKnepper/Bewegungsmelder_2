function Zeitmessung(Dauer: number) {
    
    if (boStarteMessung == 1) {
        basic.pause(1000)
        ZeitUnbewegt += 1
        if (60 * Dauer <= ZeitUnbewegt) {
            boAlarm = 1
        }
        
        if (boReset > 0 || boBewegungRegistriert > 0) {
            boAlarm = 0
            ZeitUnbewegt = 0
            boReset = 0
            boBewegungRegistriert = 0
        }
        
    }
    
}

function AlarmAusgeben(Alarm: any, Akustisch: boolean, Optisch: boolean) {
    if (Alarm) {
        if (Akustisch) {
            music.playMelody("C E C E C E ", 120)
        }
        
    }
    
    if (Optisch) {
        basic.setLedColor(0xff0000)
        basic.pause(200)
        basic.setLedColor(0x0000ff)
        basic.pause(200)
    } else {
        basic.setLedColor(0x000000)
    }
    
}

function BewegungErkennen() {
    
    //  Neuer Block (ArrayListe) wird ausgewertet
    if (zeiger_Arrays == 1) {
        basic.setLedColor(0xff00ff)
        boBewegungRegistriert = 0
        ZählerBewegungX = 0
    }
    
    //  Wurde eine Bewegung festgestellt?
    if (Math.abs(Mittelwert_X - Last_x) > SchwellwertBewegung) {
        ZählerBewegungX += 1
        serial.writeValue("Zähler+", ZählerBewegungX)
    }
    
    if (ZählerBewegungX > HäufigkeitBewegungsErkannt) {
        boBewegungRegistriert = 1
        basic.setLedColor(0x00ff00)
    }
    
    Last_x = Mittelwert_X
}

//  Fehlerquellen:
//  
//  Erschütterungen (Zugfahrt)
//  
//  Calliope fällt runter
//  
//  Calliope wird zur Seite gelegt und nicht bewegt.
function MesseBeschleunigungXYZSt(): number {
    
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
    
    boToggle = 1 - boToggle
    serial.writeValue("x", Mittelwert_X)
    serial.writeValue("Zeigerarry", zeiger_Arrays)
    BewegungErkennen()
    return 0
}

//  Programmablauf:
//  
//  Zu Beginn: Warten 100ms? Danach Bewegungsmesser starten
//  
//  Zeit starten, in der Bewegungsregistration stattfindet.
//  
//  Wenn keine Bewegung erkannt wurde (innerhalb der Zeit), dann Ausgabe
//  
//  Reset der Ausgabe, wenn wieder Bewegung registriert wurde oder manueller Reset
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
let boToggle = 0
let WertelisteStärke : number[] = []
let WertelisteZ : number[] = []
let WertelisteY : number[] = []
let WertelisteX : number[] = []
let Mittelwert_Stärke = 0
let Mittelwert_Z = 0
let Mittelwert_Y = 0
let Last_x = 0
let Mittelwert_X = 0
let ZählerBewegungX = 0
let boBewegungRegistriert = 0
let boReset = 0
let ZeitUnbewegt = 0
let boStarteMessung = 0
let SchwellwertBewegung = 0
let HäufigkeitBewegungsErkannt = 0
let zeiger_Arrays = 0
let ArrayGröße = 0
let boArrayVoll = 0
let boAlarm = 0

boArrayVoll = 0
serial.setBaudRate(BaudRate.BaudRate115200)
ArrayGröße = 10
zeiger_Arrays = 0
//  Dauer in Minuten
let ZeitMaxUnbeweglichkeit = 1
//  Dauer in Minuten
HäufigkeitBewegungsErkannt = 5
SchwellwertBewegung = 100
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

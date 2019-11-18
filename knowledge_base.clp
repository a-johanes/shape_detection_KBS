
(deftemplate objek 
    (slot sisi (type INTEGER) (range 3 6))
)

(deftemplate sisi
    (slot from (type INTEGER))
    (slot to (type INTEGER))
    (slot length (type FLOAT))
)

(deftemplate sudut
    (slot id (type INTEGER))
    (slot degree (type FLOAT))
)

(deftemplate jumlah-paralel
    (slot jumlah (type INTEGER))
)

(deffunction sama (?first ?second ?threshold)
    (if (>= ?threshold (abs (- ?first ?second) ) )
        then (return TRUE)
        else (return FALSE)
    )
)

(deffunction not-sama (?first ?second ?threshold)
    (if (sama ?first ?second ?threshold)
        then (return FALSE)
        else (return TRUE)
    )
)

(set-strategy breadth)

(deffacts init
    (atribut "sama sisi")
)

(defrule bentuk-segitiga
    (objek (sisi 3))
    (sisi (from 1) (length ?l))
    =>
    (assert (panjang-sisi ?l))
    (assert (bentuk "segitiga"))
    (assert (atribut "lancip"))
)

(defrule bentuk-segiempat
    (objek (sisi 4))
    (sisi (from 1) (length ?l))
    =>
    (assert (panjang-sisi ?l))
    (assert (bentuk "segiempat"))
)

(defrule bentuk-segilima
    (objek (sisi 5))
    (sisi (from 1) (length ?l))
    =>
    (assert (panjang-sisi ?l))
    (assert (bentuk "segilima"))
)

(defrule bentuk-segienam
    (objek (sisi 6))
    (sisi (from 1) (length ?l))
    =>
    (assert (panjang-sisi ?l))
    (assert (bentuk "segienam"))
)

(defrule tidak-sama-sisi
    ?sama <- (atribut "sama sisi") 
    ?panjang <- (panjang-sisi ?l)
    (sisi (from ?from) (length ?l1))
    (test (not-sama ?l ?l1 5))
    =>
    (retract ?sama)
    (retract ?panjang)
    (assert (atribut "tidak beraturan"))
)

(defrule sama-kaki
    (bentuk ?segi)
    (test (neq ?segi "segilima" "segienam"))
    ?tidakberaturan <- (atribut "tidak beraturan")
    (sisi (from ?from) (to ?to))
    (sisi (from ?sisi-1-from) (length ?l1))
    (sisi (to ?sisi-2-to) (length ?l2))
    (sudut (id ?id1) (degree ?deg1))
    (sudut (id ?id2) (degree ?deg2))
    (test (eq ?id1 ?from))
    (test (eq ?id2 ?to))
    (test (neq ?id1 ?id2))
    (test (sama ?deg1 ?deg2 1))
    (test (sama ?l1 ?l2 5))
    (test (eq ?from ?sisi-2-to))
    (test (eq ?to ?sisi-1-from))    
    =>
    (retract ?tidakberaturan)
    (assert (atribut "sama kaki"))
)

(defrule tumpul  (atribut "sama sisi")
    ?lancip <- (atribut "lancip")
    (bentuk "segitiga")
    (sudut (degree ?degree))
    (test (> ?degree 91.0))
    =>
    (retract ?lancip)
    (assert (atribut "tumpul"))
)

(defrule siku-siku
    ?lancip <- (atribut "lancip")
    (bentuk "segitiga")
    (sudut (degree ?degree))
    (test (sama ?degree 90.0 1))
    =>
    (retract ?lancip)
    (assert (atribut "siku-siku"))
)

(defrule jajaran-genjang
    ?bentuk <- (bentuk "segiempat")
    (jumlah-paralel (jumlah 2))
    (sudut (degree ?deg))
    =>
    (retract ?bentuk)
    (assert (bentuk "jajaran genjang"))
    (assert (atribut "beraturan"))
    (assert (besar-sudut ?deg))
)

(defrule trapesium
    ?bentuk <- (bentuk "segiempat")
    (jumlah-paralel (jumlah 1))
    =>
    (retract ?bentuk)
    (assert (bentuk "trapesium"))
)

(defrule tidak-beraturan
    ?beraturan <- (atribut "beraturan")
    (bentuk "jajaran genjang")
    (besar-sudut ?deg1)
    (sudut (degree ?deg2))
    (test (not-sama ?deg1 ?deg2 1))
    =>
    (retract ?beraturan)
)

(defrule bentuk-layang-layang
    (bentuk "jajaran genjang")
    (sisi (from ?f1) (length ?l1))
    (sisi (from ?f2) (length ?l2))
    (sisi (from ?f3) (length ?l3))
    (sisi (from ?f4) (length ?l4))
    (test (neq ?f1 ?f2 ?f3 ?f4))
    (test (neq ?f2 ?f3 ?f4))
    (test (neq ?f3 ?f4))
    (test (sama ?l1 ?l2 5))
    (test (sama ?l1 ?l3 5))
    (test (sama ?l1 ?l4 5))
    (sudut (id ?id1) (degree ?deg1))
    (sudut (id ?id2) (degree ?deg2))
    (sudut (id ?id3) (degree ?deg3))
    (sudut (id ?id4) (degree ?deg4))
    (test (neq ?id1 ?id2 ?id3 ?id4))
    (test (neq ?id2 ?id3 ?id4))
    (test (neq ?id3 ?id4))
    (test (sama ?deg1 ?deg2 1))
    (test (sama ?deg3 ?deg4 1))
    (test (not-sama ?deg1 ?deg3 1))
    =>
    (assert (atribut "bentuk layang-layang"))
)

(defrule rata-kiri
    ?tidakberaturan <- (atribut "tidak beraturan")
    (bentuk "trapesium")
    (sudut (id ?id1) (degree ?deg1))
    (sudut (id ?id2) (degree ?deg2))
    (sudut (id ?id3) (degree ?deg3))
    (sudut (id ?id4) (degree ?deg4))    
    (test (neq ?id1 ?id2 ?id3 ?id4))
    (test (neq ?id2 ?id3 ?id4))
    (test (neq ?id3 ?id4))
    (test (sama ?deg1 90.0 1))
    (test (sama ?deg2 90.0 1))
    (test (eq ?id4 (mod (+ ?id3 1) 4)))
    (test (< ?deg3 90.0))
    (test (> ?deg4 90.0))
    =>
    (retract ?tidakberaturan)
    (assert (atribut "rata-kiri"))
)

(defrule rata-kanan
    ?tidakberaturan <- (atribut "tidak beraturan")
    (bentuk "trapesium")
    (sudut (id ?id1) (degree ?deg1))
    (sudut (id ?id2) (degree ?deg
    ; (atribut "sama sisi")2))
    (sudut (id ?id3) (degree ?deg3))
    (sudut (id ?id4) (degree ?deg4))
    (test (neq ?id1 ?id2 ?id3 ?id4))
    (test (neq ?id2 ?id3 ?id4))
    (test (neq ?id3 ?id4))
    (test (sama ?deg1 90.0 1))
    (test (sama ?deg2 90.0 1))
    (test (eq ?id3 (mod (+ ?id4 1) 4)))
    (test (< ?deg3 90.0))
    (test (> ?deg4 90.0))
    =>
    (retract ?tidakberaturan)
    (assert (atribut "rata-kanan"))
)

(defrule print-solusi
    (tes ?id)
    (bentuk ?bentuk)
    (atribut ?atribut)
    =>
    (printout t "tes id: " ?id crlf)
    (printout t "bentuk: " ?bentuk crlf)
    (printout t "atribut: " ?atribut crlf)
)

(reset)

;  testing

;  segitiga sama sisi
; (assert (tes 1))
; (assert (objek (sisi 3)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 1) (length 20.0)))
; (assert (sudut (id 1) (degree 60.0)))
; (assert (sudut (id 2) (degree 60.0)))
; (assert (sudut (id 3) (degree 60.0)))

;  segitiga lancip
; (assert (tes 2))
; (assert (objek (sisi 3)))
; (assert (sisi (from 1) (to 2) (length 300.0)))
; (assert (sisi (from 2) (to 3) (length 200.0)))
; (assert (sisi (from 3) (to 1) (length 350.0)))
; (assert (sudut (id 1) (degree 58.8)))
; (assert (sudut (id 2) (degree 34.8)))
; (assert (sudut (id 3) (degree 86.4)))

; segitiga tumpul
; (assert (tes 3))
; (assert (objek (sisi 3)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 1) (length 20.0)))
; (assert (sudut (id 1) (degree 39.6)))
; (assert (sudut (id 2) (degree 121.8)))
; (assert (sudut (id 3) (degree 18.6)))

; segitiga siku-siku
; (assert (tes 4))
; (assert (objek (sisi 3)))
; (assert (sisi (from 1) (to 2) (length 30.0)))
; (assert (sisi (from 2) (to 3) (length 40.0)))
; (assert (sisi (from 3) (to 1) (length 50.0)))
; (assert (sudut (id 1) (degree 36.9)))
; (assert (sudut (id 2) (degree 53.1)))
; (assert (sudut (id 3) (degree 90.0)))

; segitiga sama kaki lancip
; (assert (tes 5))
; (assert (objek (sisi 3)))
; (assert (sisi (from 1) (to 2) (length 50.0)))
; (assert (sisi (from 2) (to 3) (length 40.0)))
; (assert (sisi (from 3) (to 1) (length 50.0)))
; (assert (sudut (id 1) (degree 47.2)))
; (assert (sudut (id 2) (degree 66.4)))
; (assert (sudut (id 3) (degree 66.4)))

; segitiga sama kaki tumpul
; (assert (tes 6))
; (assert (objek (sisi 3)))
; (assert (sisi (from 1) (to 2) (length 50.0)))
; (assert (sisi (from 2) (to 3) (length 80.0)))
; (assert (sisi (from 3) (to 1) (length 50.0)))
; (assert (sudut (id 1) (degree 106.2)))
; (assert (sudut (id 2) (degree 36.9)))
; (assert (sudut (id 3) (degree 36.9)))

; segitiga sama kaki siku-siku
; (assert (tes 7))
; (assert (objek (sisi 3)))
; (assert (sisi (from 1) (to 2) (length 50.0)))
; (assert (sisi (from 2) (to 3) (length 71.0)))
; (assert (sisi (from 3) (to 1) (length 50.0)))
; (assert (sudut (id 1) (degree 90.0)))
; (assert (sudut (id 2) (degree 45.0)))
; (assert (sudut (id 3) (degree 45.0)))

; segiempat tidak beraturan
; (assert (tes 8))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 40.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 1) (length 20.0)))
; (assert (jumlah-paralel (jumlah 0)))
; (assert (sudut (id 1) (degree 90.0)))
; (assert (sudut (id 2) (degree 120.0)))
; (assert (sudut (id 3) (degree 30.0)))
; (assert (sudut (id 4) (degree 120.0)))

; jajaran genjang (jajar genjang)
; (assert (tes 9))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 40.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 1) (length 20.0)))
; (assert (jumlah-paralel (jumlah 2)))
; (assert (sudut (id 1) (degree 60.0)))
; (assert (sudut (id 2) (degree 120.0)))
; (assert (sudut (id 3) (degree 60.0)))
; (assert (sudut (id 4) (degree 120.0)))

; jajaran genjang (persegi panjang)
; (assert (tes 10))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 40.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 1) (length 20.0)))
; (assert (jumlah-paralel (jumlah 2)))
; (assert (sudut (id 1) (degree 90.0)))
; (assert (sudut (id 2) (degree 90.0)))
; (assert (sudut (id 3) (degree 90.0)))
; (assert (sudut (id 4) (degree 90.0)))

; jajaran genjang beraturan
; (assert (tes 11))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 4) (length 20.0)))
; (assert (sisi (from 4) (to 1) (length 20.0)))
; (assert (jumlah-paralel (jumlah 2)))
; (assert (sudut (id 1) (degree 90.0)))
; (assert (sudut (id 2) (degree 90.0)))
; (assert (sudut (id 3) (degree 90.0)))
; (assert (sudut (id 4) (degree 90.0)))

; jajaran genjang berbentuk layang layang
; (assert (tes 12))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 4) (length 20.0)))
; (assert (sisi (from 4) (to 1) (length 20.0)))
; (assert (jumlah-paralel (jumlah 2)))
; (assert (sudut (id 1) (degree 60.0)))
; (assert (sudut (id 2) (degree 120.0)))
; (assert (sudut (id 3) (degree 60.0)))
; (assert (sudut (id 4) (degree 120.0)))

; trapesium sembarang
; (assert (tes 13))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 30.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 1) (length 20.0)))
; (assert (jumlah-paralel (jumlah 1)))
; (assert (sudut (id 1) (degree 120.0)))
; (assert (sudut (id 2) (degree 130.0)))
; (assert (sudut (id 3) (degree 55.0)))
; (assert (sudut (id 4) (degree 65.0)))

; trapesium sama kaki
; (assert (tes 14))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 30.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 1) (length 30.0)))
; (assert (jumlah-paralel (jumlah 1)))
; (assert (sudut (id 1) (degree 120.0)))
; (assert (sudut (id 2) (degree 120.0)))
; (assert (sudut (id 3) (degree 60.0)))
; (assert (sudut (id 4) (degree 60.0)))

; trapesium rata kiri
; (assert (tes 15))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 1) (length 30.0)))
; (assert (jumlah-paralel (jumlah 1)))
; (assert (sudut (id 1) (degree 120.0)))
; (assert (sudut (id 2) (degree 90.0)))
; (assert (sudut (id 3) (degree 90.0)))
; (assert (sudut (id 4) (degree 60.0)))

; trapesium rata kanan
; (assert (tes 16))
; (assert (objek (sisi 4)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 30.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 1) (length 20.0)))
; (assert (jumlah-paralel (jumlah 1)))
; (assert (sudut (id 1) (degree 90.0)))
; (assert (sudut (id 2) (degree 120.0)))
; (assert (sudut (id 3) (degree 60.0)))
; (assert (sudut (id 4) (degree 90.0)))

; segilima tidak beraturan
; (assert (tes 17))
; (assert (objek (sisi 5)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 40.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 5) (length 20.0)))
; (assert (sisi (from 5) (to 1) (length 20.0)))
; (assert (sudut (id 1) (degree 72.0)))
; (assert (sudut (id 2) (degree 72.0)))
; (assert (sudut (id 3) (degree 72.0)))
; (assert (sudut (id 4) (degree 72.0)))
; (assert (sudut (id 5) (degree 72.0)))

; segilima sama sisi
; (assert (tes 18))
; (assert (objek (sisi 5)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 4) (length 20.0)))
; (assert (sisi (from 4) (to 5) (length 20.0)))
; (assert (sisi (from 5) (to 1) (length 20.0)))
; (assert (sudut (id 1) (degree 72.0)))
; (assert (sudut (id 2) (degree 72.0)))
; (assert (sudut (id 3) (degree 72.0)))
; (assert (sudut (id 4) (degree 72.0)))
; (assert (sudut (id 5) (degree 72.0)))

; segienam tidak beraturan
; (assert (tes 19))
; (assert (objek (sisi 6)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 40.0)))
; (assert (sisi (from 3) (to 4) (length 40.0)))
; (assert (sisi (from 4) (to 5) (length 20.0)))
; (assert (sisi (from 5) (to 6) (length 20.0)))
; (assert (sisi (from 6) (to 1) (lenth 20.0)))
; (assert (sudut (id 1) (degree 60.0)))
; (assert (sudut (id 2) (degree 60.0)))
; (assert (sudut (id 3) (degree 60.0)))
; (assert (sudut (id 4) (degree 60.0)))
; (assert (sudut (id 5) (degree 60.0)))
; (assert (sudut (id 6) (degree 60.0)))

; segienam sama sisi
; (assert (tes 20))
; (assert (objek (sisi 6)))
; (assert (sisi (from 1) (to 2) (length 20.0)))
; (assert (sisi (from 2) (to 3) (length 20.0)))
; (assert (sisi (from 3) (to 4) (length 20.0)))
; (assert (sisi (from 4) (to 5) (length 20.0)))
; (assert (sisi (from 5) (to 6) (length 20.0)))
; (assert (sisi (from 6) (to 1) (lenth 20.0)))
; (assert (sudut (id 1) (degree 60.0)))
; (assert (sudut (id 2) (degree 60.0)))
; (assert (sudut (id 3) (degree 60.0)))
; (assert (sudut (id 4) (degree 60.0)))
; (assert (sudut (id 5) (degree 60.0)))
; (assert (sudut (id 6) (degree 60.0)))

; (agenda)
; (facts)
; (run)
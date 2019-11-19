
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

(deftemplate paralel
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

; (set-strategy breadth)

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
    (assert (hit-rule "bentuk-segitiga"))
)

(defrule bentuk-segiempat
    (objek (sisi 4))
    (sisi (from 1) (length ?l))
    =>
    (assert (panjang-sisi ?l))
    (assert (bentuk "segiempat"))
    (assert (hit-rule "bentuk-segiempat"))
)

(defrule bentuk-segilima
    (objek (sisi 5))
    (sisi (from 1) (length ?l))
    =>
    (assert (panjang-sisi ?l))
    (assert (bentuk "segilima"))
    (assert (hit-rule "bentuk-segilima"))
)

(defrule bentuk-segienam
    (objek (sisi 6))
    (sisi (from 1) (length ?l))
    =>
    (assert (panjang-sisi ?l))
    (assert (bentuk "segienam"))
    (assert (hit-rule "bentuk-segienam"))
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
    (assert (hit-rule "tidak-sama-sisi"))
)

(defrule sama-kaki
    (bentuk ?segi)
    (test (neq ?segi "segilima" "segienam" "jajaran genjang"))
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
    ; (test (not-sama 90 ?deg1 ?deg2))
    (test (eq ?from ?sisi-2-to))
    (test (eq ?to ?sisi-1-from))    
    =>
    (retract ?tidakberaturan)
    (assert (atribut "sama kaki"))
    (assert (hit-rule "sama-kaki"))
)

(defrule tumpul 
    ?lancip <- (atribut "lancip")
    (bentuk "segitiga")
    (sudut (degree ?degree))
    (test (> ?degree 91.0))
    =>
    (retract ?lancip)
    (assert (atribut "tumpul"))
    (assert (hit-rule "tumpul"))
)

(defrule siku-siku
    ?lancip <- (atribut "lancip")
    (bentuk "segitiga")
    (sudut (degree ?degree))
    (test (sama ?degree 90.0 1))
    =>
    (retract ?lancip)
    (assert (atribut "siku-siku"))
    (assert (hit-rule "siku-siku"))
)

(defrule jajaran-genjang
    ?bentuk <- (bentuk "segiempat")
    (paralel (jumlah 2))
    (sudut (degree ?deg))
    =>
    (retract ?bentuk)
    (assert (bentuk "jajaran genjang"))
    (assert (atribut "beraturan"))
    (assert (besar-sudut ?deg))
    (assert (hit-rule "jajaran-genjang"))
)

(defrule trapesium
    ?bentuk <- (bentuk "segiempat")
    (paralel (jumlah 1))
    =>
    (retract ?bentuk)
    (assert (bentuk "trapesium"))
    (assert (hit-rule "trapesium"))
)

(defrule tidak-beraturan
    ?beraturan <- (atribut "beraturan")
    (bentuk "jajaran genjang")
    (besar-sudut ?deg1)
    (sudut (degree ?deg2))
    (test (not-sama ?deg1 ?deg2 1))
    =>
    (retract ?beraturan)
    (assert (hit-rule "tidak-beraturan"))
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
    (assert (hit-rule "bentuk-layang-layang"))
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
    (assert (atribut "rata kiri"))
    (assert (hit-rule "rata-kiri"))
)

(defrule rata-kanan
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
    (test (eq ?id3 (mod (+ ?id4 1) 4)))
    (test (< ?deg3 90.0))
    (test (> ?deg4 90.0))
    =>
    (retract ?tidakberaturan)
    (assert (atribut "rata kanan"))
    (assert (hit-rule "rata-kanan"))
)

(defrule print-solusi
    (tes ?id)
    (bentuk ?bentuk)
    (atribut ?atribut)
    (ans ?ans)
    =>
    (printout t "tes id: " ?id crlf)
    (printout t "bentuk: " ?bentuk crlf)
    (printout t "atribut: " ?atribut crlf)
    (printout t "ans: " ?ans crlf)
)

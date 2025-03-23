;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; FILE
;;; bp-text.asd
;;;
;;; NAME
;;; system
;;;
;;; DESCRIPTION
;;; System definition of BP-TEXT.
;;;
;;; AUTHOR
;;; Ruben Philipp <me@rubenphilipp.com>
;;;
;;; CREATED
;;; 2025-03-01
;;;
;;; $$ Last modified:  21:07:14 Sun Mar 23 2025 CET
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


(defsystem "bp-text"
  :description "Common Lisp algorithmic text generation tools."
  :version "0.0.1"
  :author "Ruben Philipp <me@rubenphilipp.com>, Fabian Bentrup"
  :license "GPL Version 2.0 or later"
  :serial t
  ;; :in-order-to ((test-op (test-op "colporter/tests")))
  :depends-on ("alexandria"
               "cl-ppcre"
               "cologne-phonetics"
               "soundex"
               "cl-ris"
               ;; "cl-yaml"
               )
  :pathname "src/"
  :components ((:file "package")
               ;; to be cont'd...
               ))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; EOF bp-text.asd

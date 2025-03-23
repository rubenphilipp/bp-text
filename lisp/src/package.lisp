;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; FILE
;;; package.lisp
;;;
;;; NAME
;;; package
;;;
;;; DESCRIPTION
;;; Package definition of BP-TEXT.
;;;
;;; AUTHOR
;;; Ruben Philipp <me@rubenphilipp.com>
;;;
;;; CREATED
;;; 2025-03-01
;;;
;;; $$ Last modified:  21:07:49 Sun Mar 23 2025 CET
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(in-package :cl-user)

(defpackage :bp-text
  (:use :common-lisp)
  (:nicknames :bp)
  (:import-from
   :alexandria
   :assoc-value
   :alist-hash-table
   :hash-table-alist
   :hash-table-keys
   :read-file-into-string)
  (:import-from
   :cl-ppcre
   :split))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; EOF package.lisp

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; FILE
;;; text-analysis-merge.lisp
;;;
;;; NAME
;;; text-analysis-merge
;;;
;;; DESCRIPTION
;;; This code analyzes text files for similarity and merges them into
;;; new text files. The similarity consists exclusively of consecutive
;;; identical word strings.
;;;
;;; AUTHOR
;;; Fabian Bentrup fabian.bentrup@outlook.de
;;;
;;; CREATED
;;; 2025-02-17
;;;
;;; $$ Last modified:  21:08:05 Sun Mar 23 2025 CET
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ****f* read-file
;;; AUTHOR
;;; Fabian Bentrup fabian.bentrup@outlook.de
;;;
;;; CREATED
;;; 2025-02-17
;;; 
;;; DESCRIPTION
;;; Reads in a text file and returns a list of words.
;;;
;;; ARGUMENTS
;;; filepath = path to .txt file
;;; 
;;; RETURN VALUE
;;; A list of strings
;;;
;;; EXAMPLE
;;; If you read in a text file with the content “Hello World!”, a call
;;; will look like this:
;;; (read-file "filepath/test.txt")
;;; ==> ("Hello" "World!")

;;; SYNOPSIS
(defun read-file (filepath)
  (with-open-file (stream filepath :if-does-not-exist nil)
    (when stream
      (loop for line = (read-line stream nil nil)
            while line
            append (cl-ppcre:split "\\s+" line)))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ****f* write-file
;;; AUTHOR
;;; Fabian Bentrup fabian.bentrup@outlook.de
;;;
;;; CREATED
;;; 2025-02-17
;;; 
;;; DESCRIPTION
;;; Outputs the list (content) as a .txt file, separated by spaces.
;;;
;;; ARGUMENTS
;;; filepath = the file path to the new .txt file to be created
;;; content = content of the .txt file
;;; 
;;; RETURN VALUE
;;; a .txt file
;;;
;;; EXAMPLE
;;; (write-file "filepath/output.txt" '("This" "is" "a" "test."))
;;; ==> a .txt file with the content "This is a test."

;;; SYNOPSIS
(defun write-file (filepath content)
  "saves content into a .txt file"
  (with-open-file (stream filepath :direction :output :if-exists :supersede)
    (format stream "~{~a ~}" content)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ****f* find-common-sequence
;;; AUTHOR
;;; Fabian Bentrup fabian.bentrup@outlook.de
;;;
;;; CREATED
;;; 2025-02-17
;;; 
;;; DESCRIPTION
;;; Compares two lists of strings to find common word sequences
;;;
;;; ARGUMENTS
;;; words1 = a list of strings
;;; words2 = another list of strings
;;; min-length = number of common words in words1 and words2
;;;
;;; RETURN VALUE
;;; a list of strings
;;;
;;; EXAMPLE
;;; (find-common-sequence '("Hello" "World" "this" "is" "lisp") '("This"
;;; "is" "lisp") 2)
;;; ==> '("this" "is")

;;; SYNOPSIS
(defun find-common-sequence (words1 words2 min-length)
  (loop for i from 0 to (- (length words1) min-length)
        do (loop for j from 0 to (- (length words2) min-length)
                 do (let ((seq1 (subseq words1 i (+ i min-length)))
                          (seq2 (subseq words2 j (+ j min-length))))
                      (when (every #'(lambda (w1 w2) 
                                       (string-equal w1 w2)) 
                                   seq1 seq2)
                        (return-from find-common-sequence
                                     (cons i
                                           (cons
                                            j
                                            min-length))))))))
  
  
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ****f* merge-texts
;;; AUTHOR
;;; Fabian Bentrup fabian.bentrup@outlook.de
;;;
;;; CREATED
;;; 2025-02-17
;;; 
;;; DESCRIPTION
;;; merges two texts, with common word sequences
;;;
;;; ARGUMENTS
;;; words1 = a list of strings
;;; words2 = another list of strings
;;; min-length = number of common words in words1 and words2
;;;
;;; RETURN VALUE
;;; a list of strings
;;;
;;; EXAMPLE
;;; (merge-texts '("Hello" "World" "this" "is" "lisp") '("This"
;;; "is" "lisp") 2)
;;; ==> '("this" "is")

;;; SYNOPSIS
(defun merge-texts (words1 words2 min-length)
  (let ((common-info (find-common-sequence words1 words2 min-length)))
    (if common-info
        (let* ((pos1 (car common-info))
               (pos2 (cadr common-info))
               (len (cddr common-info))
               (result (append (subseq words1 0 (+ pos1 len))
                              (subseq words2 (+ pos2 len)))))
          result)
        (error "No common words found"))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ****f* process-files
;;; AUTHOR
;;; Fabian Bentrup fabian.bentrup@outlook.de
;;;
;;; CREATED
;;; 2025-02-17
;;; 
;;; DESCRIPTION
;;; Reads all .txt files in the specified folder, converts the texts
;;; into a list, compares them in pairs and merges them
;;; (merge-texts). The new texts are saved as merged-1.txt, merged-2.txt, etc.
;;;
;;; ARGUMENTS
;;; directory = Location of the texts to be analyzed
;;; min-length = number of common words
;;; 
;;; RETURN VALUE
;;; new .txt files with the merged texts
;;;
;;; EXAMPLE
;;; (process-files "/filepath/testfiles/" 2)
;;; ==> .txt files with all merged texts

;;; SYNOPSIS
(defun process-files (directory min-length)
  (let* ((files (directory (merge-pathnames "*.txt" directory)))
         (texts (mapcar #'read-file files))
         (merged-texts nil))
    (loop for (t1 t2) on texts while t2
          do (handler-case
                 (push (merge-texts t1 t2 min-length) merged-texts)
               (error (e)
                 (format t "Error merging texts: ~A~%" e))))
    (loop for text in (reverse merged-texts)
          for i from 1
          do (write-file (merge-pathnames (format nil "merged-~d.txt"
                                                  i) directory) text))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; EOF 

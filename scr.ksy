meta:
    id: pkd
    application: pkd
    endian: le
seq:
    - id: magic 
      contents: ["PACK"]
    - id: filecount
      type: u4
    - id: header
      type: header
      size: 3800

types:
    header:
        seq:
            - id: entries
              size: 0x28
              repeat: expr
              repeat-expr: 95
              type: file_entry
    file_entry:
        seq:
            - id: filename
              size: 8
              type: str
              encoding: ascii
            - id: padding
              size: 20
            - id: file_size
              type: u4
            - id: file_offset
              type: u4
        instances:
              body:
                pos: file_offset
                size: file_size
                io: _root._io

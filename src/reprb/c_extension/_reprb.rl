#include <Python.h>
#define PY_SSIZE_T_CLEAN

char HEX[16] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
unsigned char HEXV [256] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13, 14, 15, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 10, 11, 12, 13, 14, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};


%%{
    machine c_reprb_fsm;

    escape = 0x5c;
    normal = ((0x20 .. 0x7e) - escape)  @ { *buf++ =  fc;};
    
    special_escape = (
              0x0  @ { *buf++ =  '0'; }
            | 0x7  @ { *buf++ =  'a'; }
            | 0x8  @ { *buf++ =  'b'; }
            | 0x9  @ { *buf++ =  't'; }
            | 0xa  @ { *buf++ =  'n'; }
            | 0xc  @ { *buf++ =  'f'; }
            | 0xd  @ { *buf++ =  'r'; }
            | 0x5c @ { *buf++ =  '\\';}
        ) > { *buf++ =  '\\'; };

    need_escape = (any - (normal | special_escape))
    @{
        *buf++ =  '\\'; 
        *buf++ =  'x'; 
        *buf++ = HEX[fc >> 4];
        *buf++ = HEX[fc & 0xF];
    };

    octet = normal | need_escape | special_escape;

    main := octet*;

}%%

%% write data;

PyObject* c_reprb(PyObject* self, PyObject* args) {
    PyObject* bytes_obj;
    if (!PyArg_ParseTuple(args, "O", &bytes_obj)) {
        return NULL;
    }
    if (!PyBytes_Check(bytes_obj)) {
        PyErr_SetString(PyExc_TypeError, "Expected a bytes object");
        return NULL;
    }

    unsigned char* input_bytes = (unsigned char*)PyBytes_AS_STRING(bytes_obj);
    Py_ssize_t input_length = PyBytes_GET_SIZE(bytes_obj);
	
    unsigned char* buf = (unsigned char*)malloc(input_length * 4);  
    if (buf == NULL) {
        return NULL;
    }
    unsigned char* res = buf;
    int cs;
    unsigned char * p = input_bytes;
    unsigned char * pe = input_bytes + input_length;

    %% write init;
    %% write exec;

    size_t res_length = buf - res;
    // trans to python bytes object
    PyObject* py_bytes = Py_BuildValue("y#", res, res_length);

    // release 
    free(res);  

    return py_bytes;
}

%%{
    machine c_evals_fsm;

    escape = 0x5c;
    
    escape_sequence =  escape (
        escape  @ { value = '\\';}
        |'t'    @ { value = '\t';}
        |'b'    @ { value = '\b';}
        |'n'    @ { value = '\n';}
        |'r'    @ { value = '\r';}
        |'v'    @ { value = '\v';}
        |'f'    @ { value = '\f';}
        |'a'    @ { value = '\a';}
        |'0'    @ { value = 0   ;}
        |'x'    @ { value = 0   ;} xdigit{2} ${value = (value<<4) + HEXV[fc];}
    );

    main := |*
        (any - escape)+                      { cp_len = p + 1 - ts; memcpy(buf, ts, cp_len); buf+= cp_len;};
        escape_sequence                      { *buf++ = value;};
        escape                               { *buf++ = fc;};
    *|;
}%%

%% write data;

PyObject* c_evalb(PyObject* self, PyObject* args) {
    PyObject* bytes_obj;
    if (!PyArg_ParseTuple(args, "O", &bytes_obj)) {
        return NULL;
    }
    if (!PyBytes_Check(bytes_obj)) {
        PyErr_SetString(PyExc_TypeError, "Expected a bytes object");
        return NULL;
    }

    unsigned char* input_bytes = (unsigned char*)PyBytes_AS_STRING(bytes_obj);
    Py_ssize_t input_length = PyBytes_GET_SIZE(bytes_obj);
    unsigned char* buf = (unsigned char*)malloc(input_length);  
    if (buf == NULL) {
        return NULL;
    }

    unsigned char* res = buf;
    int cs;
    unsigned char *  ts;
    unsigned char *  te;
    int cp_len;
    unsigned char value = 0;
    unsigned char * p = input_bytes;
    unsigned char * pe = input_bytes + input_length;
    unsigned char * eof = pe;

    %% write init;
    %% write exec;

    size_t res_length = buf - res;
    // trans to python bytes object
    PyObject* py_bytes = Py_BuildValue("y#", res, res_length);

    // release 
    free(res);  

    return py_bytes;
}

static PyMethodDef Methods[] = {
    {"c_reprb", c_reprb, METH_VARARGS, "repr bytes"},
    {"c_evalb", c_evalb, METH_VARARGS, "eval bytes"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_reprb",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit__reprb(void) {
    return PyModule_Create(&module);
}
python_callbacks = {}

function set_exec(exec) {
    // Not supported to do item assignment of JS objects in python, but functions can be ran
    python_callbacks.exec = exec;
}

function py_exec(code) {
    // Executes code with the exec function passed from python
    python_callbacks.exec(code);
}

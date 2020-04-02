CREATE TABLE paciente
(
    nombre_pac varchar(50),
    rut_pac integer,
    f_nacimiento date,
    primary key (rut_pac)
);

CREATE TABLE vacuna
(
    nombre_enfermedad varchar(50),
    f_ingreso date,
    PRIMARY KEY (nombre_enfermedad)
);

CREATE TABLE recibe_vacuna
(
    rut_pac integer,
    nombre_enfermedad varchar(50),
    fecha_vacuna date,
    FOREIGN KEY (rut_pac) REFERENCES paciente(rut_pac),
    FOREIGN KEY (nombre_enfermedad) REFERENCES vacuna(nombre_enfermedad)
);

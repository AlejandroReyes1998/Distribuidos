<?php
$telefono=$_REQUEST['txtTelefono'];
$direccion=$_REQUEST['txtaDireccion'];
$nombre=$_REQUEST['txtNombre'];
$apellidop=$_REQUEST['txtApellidoP'];
$apellidom=$_REQUEST['txtApellidoM'];
$matricula=$_REQUEST['txtMatricula'];
$email=$_REQUEST['txtEmail'];
$year=$_REQUEST['txtYearNacimiento'];
echo "Hola, <b><i> $nombre $apellidop $apellidom </b></i><br>";
echo "Bienvenido al curso de PHP, confirmaremos tus datos<br>";
echo "Son los siguientes:<br>";
echo "<b>Matricula: $matricula</b>";
echo "<b>E-Mail: $email</b>";
echo "<b>Telefono: $telefono</b>";
echo "<b>Fecha de nacimiento: $year</b>";
echo "<table width='400' height='20' border='0' >
     <td bgcolor='FFEB99'>Direccion: $direccion</td></table>";
?>
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-05-2025 a las 18:26:22
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dbproyecto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_autores`
--

CREATE TABLE `t_autores` (
  `aut_id` int(11) NOT NULL,
  `aut_uid` text NOT NULL,
  `aut_nombre` text NOT NULL,
  `aut_estado` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_autores`
--

INSERT INTO `t_autores` (`aut_id`, `aut_uid`, `aut_nombre`, `aut_estado`) VALUES
(3, '3dd6c21a-ecc1-407f-b01a-57aeb1337e59', 'elkin', '1'),
(4, '13be681a-6695-4134-9d13-ed7c291f3d62', 'dolcey', '0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_categorias`
--

CREATE TABLE `t_categorias` (
  `cat_id` int(11) NOT NULL,
  `cat_uid` text NOT NULL,
  `cat_tipo` varchar(255) NOT NULL,
  `cat_estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_categorias`
--

INSERT INTO `t_categorias` (`cat_id`, `cat_uid`, `cat_tipo`, `cat_estado`) VALUES
(1, '7995c7c4-6410-4d03-ba28-6f1ad576cee6', 'matematicas', 0),
(2, '9ef2bc04-283a-47b3-a42c-637798d00555', 'ingles', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_usuarios`
--

CREATE TABLE `t_usuarios` (
  `id` int(11) NOT NULL,
  `uid` text NOT NULL,
  `primer_nombre` varchar(255) NOT NULL,
  `segundo_nombre` varchar(255) DEFAULT NULL,
  `primer_apellido` varchar(255) NOT NULL,
  `segundo_apellido` varchar(255) DEFAULT NULL,
  `estado` int(11) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `direccion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_usuarios`
--

INSERT INTO `t_usuarios` (`id`, `uid`, `primer_nombre`, `segundo_nombre`, `primer_apellido`, `segundo_apellido`, `estado`, `correo`, `telefono`, `direccion`) VALUES
(1, '8e38bd04-d13e-4a1e-9629-bdfac96fc6a6', 'Carlos', 'Andres', 'Gomez', 'Lopez', 0, 'carlos@example.com', '123456789', 'Calle 123'),
(2, '96fa55de-72d4-4a17-b77e-d59baa318307', 'Marta', 'Ines', 'Geronimo', 'Galindo', 1, 'marta@example.com', '33333333', 'calle 15'),
(3, '597f8a92-5a60-4c86-81bd-520ec4ef5b6e', 'test', NULL, 'test', NULL, 1, 'test@example.com', '11111111', 'test30');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `t_autores`
--
ALTER TABLE `t_autores`
  ADD PRIMARY KEY (`aut_id`);

--
-- Indices de la tabla `t_categorias`
--
ALTER TABLE `t_categorias`
  ADD PRIMARY KEY (`cat_id`);

--
-- Indices de la tabla `t_usuarios`
--
ALTER TABLE `t_usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `t_autores`
--
ALTER TABLE `t_autores`
  MODIFY `aut_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `t_categorias`
--
ALTER TABLE `t_categorias`
  MODIFY `cat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `t_usuarios`
--
ALTER TABLE `t_usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

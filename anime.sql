-- MySQL dump 10.13  Distrib 5.6.33, for Win64 (x86_64)
--
-- Host: localhost    Database: anime
-- ------------------------------------------------------
-- Server version	5.6.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES gbk */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `anime`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `anime` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `anime`;

--
-- Table structure for table `bangumi`
--

DROP TABLE IF EXISTS `bangumi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bangumi` (
  `title` varchar(100) DEFAULT NULL,
  `num` int(11) DEFAULT '0',
  `total_num` int(11) DEFAULT '24'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bangumi`
--

LOCK TABLES `bangumi` WRITE;
/*!40000 ALTER TABLE `bangumi` DISABLE KEYS */;
INSERT INTO `bangumi` VALUES ('斯特拉的魔法',12,12),('魔法少女育成计划',12,12),('漂流武士',12,12),('少女编号',12,12),('Euphonium',13,13),('3月的狮子',14,24),('Ajin 2',13,13),('JOJO的奇妙冒险 不灭钻石',39,39),('终末的伊泽塔',12,12),('Flip Flappers',13,13),('编舟记',11,11),('幼女战记',3,24),('亚人酱有话要说',3,24),('Urara迷路帖',3,24),('情热传说',16,26),('小林家的龙女仆',2,24),('为美好的世界献上祝福！第二季',3,24),('人渣的本愿',2,24),('小魔女学园',3,24),('废天使加百列',3,13),('猫咪日常',3,13),('One room',3,13);
/*!40000 ALTER TABLE `bangumi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `mail` varchar(30) DEFAULT NULL,
  `title` varchar(30) DEFAULT NULL,
  `num` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('542326526@qq.com','幼女战记',3),('542326526@qq.com','人渣的本愿',2),('2311956389@qq.com','小魔女学园',3),('2311956389@qq.com','小林家的龙女仆',2),('2311956389@qq.com','亚人酱有话要说',3),('2311956389@qq.com','为美好的世界献上祝福！第二季',3),('542326526@qq.com','亚人酱有话要说',3),('542326526@qq.com','小林家的龙女仆',2),('542326526@qq.com','为美好的世界献上祝福！第二季',3),('542326526@qq.com','Urara迷路帖',3),('542326526@qq.com','3月的狮子',14),('542326526@qq.com','废天使加百列',3),('542326526@qq.com','猫咪日常',3),('542326526@qq.com','One room',3);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-01-26 21:53:08

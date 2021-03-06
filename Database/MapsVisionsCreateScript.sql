USE [master]
GO
/****** Object:  Database [MapsVisions]    Script Date: 8/8/2021 1:06:02 AM ******/
CREATE DATABASE [MapsVisions]

GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [MapsVisions].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [MapsVisions] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [MapsVisions] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [MapsVisions] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [MapsVisions] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [MapsVisions] SET ARITHABORT OFF 
GO
ALTER DATABASE [MapsVisions] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [MapsVisions] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [MapsVisions] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [MapsVisions] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [MapsVisions] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [MapsVisions] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [MapsVisions] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [MapsVisions] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [MapsVisions] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [MapsVisions] SET  DISABLE_BROKER 
GO
ALTER DATABASE [MapsVisions] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [MapsVisions] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [MapsVisions] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [MapsVisions] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [MapsVisions] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [MapsVisions] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [MapsVisions] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [MapsVisions] SET RECOVERY FULL 
GO
ALTER DATABASE [MapsVisions] SET  MULTI_USER 
GO
ALTER DATABASE [MapsVisions] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [MapsVisions] SET DB_CHAINING OFF 
GO
ALTER DATABASE [MapsVisions] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [MapsVisions] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [MapsVisions] SET DELAYED_DURABILITY = DISABLED 
GO
EXEC sys.sp_db_vardecimal_storage_format N'MapsVisions', N'ON'
GO

USE [MapsVisions]
GO
/****** Object:  Table [dbo].[capture_detected_text]    Script Date: 8/8/2021 1:06:02 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[capture_detected_text](
	[capture_id] [int] NOT NULL,
	[word_num] [int] NOT NULL,
	[EffectsType] [nvarchar](50) NOT NULL,
	[page_num] [int] NULL,
	[line_num] [int] NULL,
	[word_num_inline] [int] NULL,
	[left] [int] NULL,
	[top] [int] NULL,
	[width] [int] NULL,
	[height] [int] NULL,
	[confidence] [decimal](5, 2) NULL,
	[Word] [nvarchar](150) NULL,
	[CWord] [nvarchar](150) NULL,
	[MDegree] [decimal](5, 2) NULL,
 CONSTRAINT [PK_capture_detected_text] PRIMARY KEY CLUSTERED 
(
	[capture_id] ASC,
	[word_num] ASC,
	[EffectsType] ASC
)
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[cities]    Script Date: 8/8/2021 1:06:02 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[cities](
	[id] [int] NOT NULL,
	[city] [nvarchar](150) NOT NULL,
	[lat] [float] NOT NULL,
	[lng] [float] NOT NULL,
	[iso2] [nvarchar](50) NOT NULL,
	[iso3] [nvarchar](50) NOT NULL,
	[city_ascii] [nvarchar](150) NOT NULL,
	[admin_name] [nvarchar](150) NULL,
	[capital] [nvarchar](50) NULL,
	[population] [float] NULL,
	[country_id] [int] NULL,
 CONSTRAINT [PK_cities2] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[continents]    Script Date: 8/8/2021 1:06:02 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[continents](
	[code] [char](2) NOT NULL,
	[name] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[code] ASC
)
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[countries]    Script Date: 8/8/2021 1:06:02 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[countries](
	[country_id] [int] NOT NULL,
	[code] [char](2) NOT NULL,
	[name] [varchar](64) NOT NULL,
	[full_name] [varchar](128) NOT NULL,
	[iso3] [char](3) NOT NULL,
	[number] [int] NOT NULL,
	[continent_code] [char](2) NOT NULL,
	[display_order] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[country_id] ASC
) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[code] ASC
)
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[location_photos]    Script Date: 8/8/2021 1:06:02 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[location_photos](
	[capture_id] [int] IDENTITY(1,1) NOT NULL,
	[lat] [decimal](12, 8) NULL,
	[lng] [decimal](12, 8) NULL,
	[map_provider] [nchar](2) NULL,
	[capture_url] [nvarchar](250) NULL,
	[quarter] [nchar](11) NULL,
	[main_capture_id] [int] NULL,
	[city_code] [int] NULL,
 CONSTRAINT [PK_location_photos] PRIMARY KEY CLUSTERED 
(
	[capture_id] ASC
)
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[locations]    Script Date: 8/8/2021 1:06:02 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[locations](
	[lat] [decimal](12, 8) NOT NULL,
	[lng] [decimal](12, 8) NOT NULL,
	[map_provider] [nchar](2) NULL,
	[city_code] [int] NULL,
	[state] [nvarchar](150) NULL,
	[area] [nvarchar](150) NULL,
	[location_type] [nvarchar](50) NULL,
	[location_details] [nvarchar](250) NULL,
 CONSTRAINT [PK_locations] PRIMARY KEY CLUSTERED 
(
	[lat] ASC,
	[lng] ASC
)
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[continents] ADD  DEFAULT (NULL) FOR [name]
GO
ALTER TABLE [dbo].[countries] ADD  DEFAULT ('900') FOR [display_order]
GO
ALTER TABLE [dbo].[cities]  WITH CHECK ADD  CONSTRAINT [FK_cities_countries] FOREIGN KEY([country_id])
REFERENCES [dbo].[countries] ([country_id])
GO
ALTER TABLE [dbo].[cities] CHECK CONSTRAINT [FK_cities_countries]
GO
ALTER TABLE [dbo].[countries]  WITH CHECK ADD  CONSTRAINT [continents_countries_fk] FOREIGN KEY([continent_code])
REFERENCES [dbo].[continents] ([code])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[countries] CHECK CONSTRAINT [continents_countries_fk]
GO
ALTER TABLE [dbo].[location_photos]  WITH CHECK ADD  CONSTRAINT [FK_location_photos_cities] FOREIGN KEY([city_code])
REFERENCES [dbo].[cities] ([id])
GO
ALTER TABLE [dbo].[location_photos] CHECK CONSTRAINT [FK_location_photos_cities]
GO
ALTER TABLE [dbo].[location_photos]  WITH CHECK ADD  CONSTRAINT [FK_location_photos_locations] FOREIGN KEY([lat], [lng])
REFERENCES [dbo].[locations] ([lat], [lng])
GO
ALTER TABLE [dbo].[location_photos] CHECK CONSTRAINT [FK_location_photos_locations]
GO
ALTER TABLE [dbo].[location_photos]  WITH CHECK ADD  CONSTRAINT [FK_location_photos_main_location_photos] FOREIGN KEY([main_capture_id])
REFERENCES [dbo].[location_photos] ([capture_id])
GO
ALTER TABLE [dbo].[location_photos] CHECK CONSTRAINT [FK_location_photos_main_location_photos]
GO
ALTER TABLE [dbo].[locations]  WITH CHECK ADD  CONSTRAINT [FK_locations_cities] FOREIGN KEY([city_code])
REFERENCES [dbo].[cities] ([id])
GO
ALTER TABLE [dbo].[locations] CHECK CONSTRAINT [FK_locations_cities]
GO
USE [master]
GO
ALTER DATABASE [MapsVisions] SET  READ_WRITE 
GO

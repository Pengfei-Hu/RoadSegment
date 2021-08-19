﻿using MapsVisionsAPI.Data.Entities;
using MapsVisionsAPI.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Data
{
    public class MapsVisionsDbContext : DbContext
    {

            public MapsVisionsDbContext(DbContextOptions<MapsVisionsDbContext> options) : base(options)
            {

            }
            public DbSet<MapImageRecogResults> MapImageRecogResults { get; set; }
            public DbSet<Location_Photos> Location_Photos { get; set; }

    }

}

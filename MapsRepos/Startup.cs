using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using MapsRepos.Data;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Http.Features;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.FileProviders;
using System.IO;

namespace MapsRepos
{
    public class Startup
    {
        readonly string AllowMapsUIOrigins = "_myAllowSpecificOrigins";
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors(options =>
            {
                options.AddPolicy(name: AllowMapsUIOrigins,
                                  builder =>
                                  {
                                      builder.WithOrigins("http://localhost:8000")
                                        .AllowAnyHeader()
                                        .AllowAnyMethod(); ;
                                  });
            });

            services.AddControllers();
            services.Configure<FormOptions>(form => {
                form.ValueLengthLimit = int.MaxValue;
                form.MultipartBodyLengthLimit = 268435456;
                form.MemoryBufferThreshold = int.MaxValue;
            });
            services.AddDbContext<MapsVisionsDbContext>(options =>
            {
                options.UseSqlServer(Configuration.GetConnectionString("MapsVisionsDbConnection"));
            });

            //services.AddDatabaseDeveloperPageExceptionFilter();

            services.AddControllersWithViews();

        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            app.UseStaticFiles();
            app.UseStaticFiles(new StaticFileOptions()
            {
                FileProvider = new PhysicalFileProvider(Path.Combine(Directory.GetCurrentDirectory(), @"Resources")),
                RequestPath = new PathString("/Resources")
            });
            app.UseCors(AllowMapsUIOrigins);

            app.UseHttpsRedirection();

            app.UseRouting();

            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}

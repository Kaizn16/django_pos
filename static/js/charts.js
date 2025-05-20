document.addEventListener('DOMContentLoaded', () => {
  const topCategoriesOptions = {
    chart: { 
      type: 'pie', 
      height: '100%',
      width: '100%',
      toolbar: { show: false }
    },
    labels: ['Electronics', 'Books', 'Clothing', 'Home Appliances', 'Sports'],
    series: [44, 25, 15, 10, 6],
    legend: { position: 'right' },
    responsive: [
      { 
        breakpoint: 640, 
        options: { 
          chart: {
            width: '100%',
            height: '100%',
          },
          legend: { position: 'bottom' }
        }
      }
    ],
  };

  const productSalesOptions = {
    chart: { 
      type: 'bar', 
      height: '100%',  
      width: '100%',
      toolbar: { show: false }
    },
    series: [{ name: 'Sales', data: [80, 60, 50, 40, 30] }],
    xaxis: { categories: ['iPhone', 'Harry Potter', 'T-Shirt', 'Microwave', 'Football'] },
    plotOptions: { bar: { borderRadius: 4 } },
    responsive: [
      { 
        breakpoint: 640, 
        options: { 
          chart: {
            width: '100%',
            height: '100%',
          },
          legend: { position: 'bottom' }
        }
      }
    ],
  };

  new ApexCharts(document.querySelector("#topCategoriesChart"), topCategoriesOptions).render();
  new ApexCharts(document.querySelector("#productSalesChart"), productSalesOptions).render();
});

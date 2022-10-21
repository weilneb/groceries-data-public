import { Container, Typography } from '@mui/material';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2
import React, { useEffect, useState } from 'react';
import { Chart } from './Chart.js';
import getProducts from './GetProducts.js';
import Divider from '@mui/material/Divider';

function App() {
  const [productsByCategory, setProductsByCategory] = useState(null);
  useEffect(() => {
    getProducts((products) => {
      console.log(products);
      setProductsByCategory(products);
    })
  }, []);
  return (<Container maxWidth={'lg'}>
    <Grid>
      <Typography variant='h2' sx={{ fontWeight: 'medium' }}>Groceries Price History</Typography>
    </Grid>
    <Divider />
    {productsByCategory === null && 'Loading...'}
    {productsByCategory !== null && Object.entries(productsByCategory).map(([category, products]) => {
      return <Grid container key={category} py={3} rowSpacing={2} columnSpacing={2}>
        <Grid item xs={12} key={`${category}-title`}>
          <Typography variant='h3' sx={{ fontWeight: 'regular' }}>{category}</Typography>
        </Grid>
        {products.map(product => 
          <Grid item xs={12} md={6}>
            <Chart product={product} key={product.id} />
          </Grid>
          )}
      </Grid>

    }).reduce((a, b) => [a, <Divider />, b])}

  </Container>);
}


export default App;

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
  return (<Container maxWidth={false} disableGutters>
    <Grid>
      <Typography variant='h2' sx={{fontWeight : 'medium'}}>Groceries Price History</Typography>
    </Grid>
    <Divider/>
    {productsByCategory === null && 'Loading...'}
    {productsByCategory !== null && productsByCategory.map(d => {
      return <Grid container key={d.category} my={3} disableGutters>
        <Grid xs={12} key={`${d.category}-title`}>
          <Typography variant='h3' sx={{fontWeight : 'regular'}} py={1}>{d.category}</Typography>
        </Grid>
        {d.urls.map(url => <Chart productUrl={url} key={url} />)}
      </Grid>

    }).reduce((a, b) => [a, <Divider />, b])}

  </Container>);
}


export default App;

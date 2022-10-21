import { ResponsiveContainer, LineChart, YAxis, XAxis, Tooltip, CartesianGrid, Line } from 'recharts';
import moment from 'moment';
import Grid from '@mui/material/Unstable_Grid2';
import { Typography } from '@mui/material';
import Link from '@mui/material/Link';


export function ChartPriceTimeSeries(props) {
  return (
    <Grid container xs={12} key={props.productName}>
      <Grid item xs={12} key={`${props.productName}-title`}>
        <Link href={props.productUrl}>
            <Typography variant='h6'>{props.productName}</Typography>
        </Link>
      </Grid>
      <Grid item xs={12} key={`${props.productName}-chart`}>
        <ResponsiveContainer minHeight={350}>
          <LineChart width={'100%'} height={'100%'} margin={{ top: 20, bottom: 0, right: 20, left: 0}}
            data={props.priceData}
          >
            <XAxis dataKey="ts" domain={['dataMin', 'dataMax']} type="number" tickFormatter={(x) => moment(x).fromNow()} />
            <YAxis dataKey="price" domain={['dataMin', 'dataMax']} tickFormatter={(x) => x.toFixed(2)}/>
            <Tooltip labelFormatter={(x) => moment(x).format('MMMM Do YYYY')}
              formatter={(value, name, props) => {
                return [`$${Number(value).toFixed(2)}`];
              }} />
            <CartesianGrid stroke="#f5f5f5" />
            <Line type="monotone" dataKey="price" stroke="#189e27" yAxisId={0} />
          </LineChart></ResponsiveContainer>
      </Grid>
    </Grid>
  );
}

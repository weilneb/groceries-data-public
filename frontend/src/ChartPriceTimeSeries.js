import { ResponsiveContainer, LineChart, YAxis, XAxis, Tooltip, CartesianGrid, Line } from 'recharts';
import moment from 'moment';
import Grid from '@mui/material/Unstable_Grid2';
import { Typography } from '@mui/material';
import Link from '@mui/material/Link';


export function ChartPriceTimeSeries(props) {
  return (
    <Grid container xs={12} md={6} key={props.productName}>
      <Grid container key={`${props.productName}-title`}>
        <Link href={props.productUrl}>
            <Typography variant='h6'>{props.productName}</Typography>
        </Link>
      </Grid>
      <Grid container key={`${props.productName}-chart`}>
        <ResponsiveContainer width='100%' minWidth={600} height={300}>
          <LineChart margin={{ top: 20, bottom: 20, right: 20, left: 20}}
            data={props.priceData}
          >
            <XAxis dataKey="ts" scale="time" tickFormatter={(x) => moment(x).fromNow()} />
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

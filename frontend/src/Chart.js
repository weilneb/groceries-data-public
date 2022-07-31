
import React, { useEffect, useState } from 'react';
import moment from 'moment';
import { ChartPriceTimeSeries } from './ChartPriceTimeSeries';

const BASE_URL = 'https://wzoujjhpbc.execute-api.ap-southeast-2.amazonaws.com/dev/groceries/price-history'

function priceHistoryUrl(productUrl) {
  const params = new URLSearchParams({ url: productUrl });
  return `${BASE_URL}?${params}`;
}

function transformData(timeData) {
  return timeData.map(x => {
    return { ts: moment(x.timestamp).valueOf(), ...x };
  });
}

export function Chart(props) {
  const [data, setData] = useState(null);
  const url = priceHistoryUrl(props.productUrl);
  useEffect(
    () => {
      fetch(url)
        .then(response => response.json())
        .then(json_data => {
          setData(transformData(json_data));
        });
    }, [url]
  )

  function loadedChart() {
    const productName = data[0].name;
    const productUrl = data[0].url;
    return <ChartPriceTimeSeries priceData={data} productName={productName} productUrl={productUrl} key={productName} />;
  }

  return (
    <div>
      {data === null && 'Loading...'}
      {data !== null && loadedChart()}
    </div>
  )
}


import React, { useEffect, useState } from 'react';
import moment from 'moment';
import { ChartPriceTimeSeries } from './ChartPriceTimeSeries';
import getRestApiBaseUrl from './config';


function priceHistoryUrl(productId) {
  const params = new URLSearchParams({ id: productId });
  return `${getRestApiBaseUrl()}/groceries/price-history?${params}`;
}

function transformData(timeData) {
  return timeData.map(x => {
    // moment() parses iso-8601: https://momentjs.com/guides/#/parsing/
    // valueOf() gives unix milliseconds: https://momentjs.com/docs/#/displaying/unix-timestamp-milliseconds/
    return { ts: moment(x.timestamp).valueOf(), ...x };
  });
}

export function Chart(props) {
  const [data, setData] = useState(null);
  const {product} = props;
  const url = priceHistoryUrl(product.id);
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
    return <ChartPriceTimeSeries priceData={data} productName={product.name} productUrl={product.url} key={product.url} />;
  }

  return (
    <div>
      {data === null && 'Loading...'}
      {data !== null && loadedChart()}
    </div>
  )
}

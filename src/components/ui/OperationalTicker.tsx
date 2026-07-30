import "../../styles/components/OperationalTicker.css";

const TICKER_ITEMS = [
  <>
    <b>SIGEC v2</b> ARTs processed: <b>1,142,338</b>
  </>,
  <>
    last block · <b>#0x3f7a91</b> · 12s ago
  </>,
  <>
    FiscalBot · cron · <b>mon 06:00 BRT</b>
  </>,
  <>
    Sentinel-2 tiles · <b>20 reservoirs · NDWI ok</b>
  </>,
  <>
    systemd · <b>8/8 services up</b>
  </>,
  <>
    Cloudflare Tunnel · <b>edge: gru</b> · <b>43 ms</b>
  </>,
];

export function OperationalTicker() {
  return (
    <section className="operational-ticker" aria-label="Operational engineering highlights">
      <div className="operational-ticker__viewport">
        <div className="operational-ticker__track">
          {[...TICKER_ITEMS, ...TICKER_ITEMS].map((item, index) => (
            <span className="operational-ticker__item" key={index}>
              {item}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}

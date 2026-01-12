import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    np.random.seed(42)

    periods = 3600
    rng = pd.date_range('2023-01-01 12:00', periods=periods, freq='s')

    normal_traffic = np.random.normal(loc=500, scale=50, size=periods)
    normal_traffic = np.maximum(normal_traffic, 0)

    df = pd.DataFrame({'timestamp': rng, 'traffic_kbps': normal_traffic})
    df.set_index('timestamp', inplace=True)

    anomali_noktalari = [600, 1800, 3000] 
    for start in anomali_noktalari:
        duration = 20
        df.iloc[start:start+duration, 0] += np.random.normal(loc=1500, scale=100, size=duration)

    window_size = 60 
    sigma_factor = 3

    df['moving_avg'] = df['traffic_kbps'].rolling(window=window_size).mean()
    df['moving_std'] = df['traffic_kbps'].rolling(window=window_size).std()

    df['upper_threshold'] = df['moving_avg'] + (sigma_factor * df['moving_std'])

    df['detected_anomaly'] = df['traffic_kbps'] > df['upper_threshold']
    df['detected_anomaly'].fillna(False, inplace=True)

    plt.figure(figsize=(14, 7))

    plt.plot(df.index, df['traffic_kbps'], label='Trafik (kbps)', color='#1f77b4', alpha=0.6)

    plt.plot(df.index, df['upper_threshold'], label=f'Eşik Değeri (Mean + {sigma_factor}$\sigma$)', 
            color='orange', linestyle='--', linewidth=2)

    anomalies = df[df['detected_anomaly']]
    plt.scatter(anomalies.index, anomalies['traffic_kbps'], color='red', 
                label='Tespit Edilen Anomali', s=50, zorder=5, edgecolors='black')

    plt.title('Ağ Trafiği Anomali Tespiti (Hedef FPR < %5)', fontsize=14)
    plt.xlabel('Zaman')
    plt.ylabel('Trafik Hacmi (kbps)')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    
if __name__ == "__main__":
    main()

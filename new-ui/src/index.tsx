import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom'
import App from './App';
import { lang } from './i18n'
import { ConfigProvider } from 'antd'

import './index.css';

import zh_CN from 'antd/lib/locale/zh_CN'
import en_US from  'antd/lib/locale/en_US'

import './mock'

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter basename="/test">
      <ConfigProvider locale={lang==='zh-CN'?zh_CN:en_US}>
        <App />
      </ConfigProvider>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

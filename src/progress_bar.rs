use std::io::{self, Write};

/// 標準ライブラリのみで動作する簡易プログレスバー
pub struct SimpleProgressBar {
    total: usize,
    width: usize,
    writer: io::Stderr, // 出力先（通常はStderr）
}

impl SimpleProgressBar {
    /// 新しいプログレスバーを作成
    pub fn new(total: usize) -> Self {
        Self {
            total,
            width: 40, // バーの幅（文字数）を固定
            writer: io::stderr(),
        }
    }

    /// 進捗を更新して描画
    pub fn update(&mut self, current: usize) {
        let mut handle = self.writer.lock(); // ロックを取得して高速化
        
        // 進捗率の計算
        let percent = current as f64 / self.total as f64;
        let filled = (percent * self.width as f64) as usize;
        
        // バーの文字列生成（無駄なアロケーションを避けるため簡易的に構築）
        // 例: [=====>          ] 45%
        write!(handle, "\r[").unwrap();
        for _ in 0..filled { write!(handle, "=").unwrap(); }
        if filled < self.width { write!(handle, ">").unwrap(); }
        for _ in 0..(self.width - filled).saturating_sub(1) { write!(handle, " ").unwrap(); }
        
        // 最後にパーセンテージを表示
        write!(handle, "] {:3.0}%", percent * 100.0).unwrap();
        handle.flush().unwrap();
    }

    /// 完了時の処理（改行を入れる）
    pub fn finish(&mut self) {
        let mut handle = self.writer.lock();
        writeln!(handle, "\nDone.").unwrap();
    }
}

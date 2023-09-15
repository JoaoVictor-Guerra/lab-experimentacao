package com.ti.lab02.ckmetric;


import com.ti.lab02.global.domain.entity.BaseEntity;
import com.ti.lab02.repo.Repository;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import static com.ti.lab02.utils.HashUtils.generateHash;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "t_ck_metric", uniqueConstraints = {
        @UniqueConstraint(name = "uk_ck_metric_hash_id", columnNames = {"hash_id"}),
        @UniqueConstraint(name = "uk_ck_metric", columnNames = {"id"})
})
@SQLDelete(sql = "UPDATE t_ck_metric SET deleted = true WHERE id = ?")
@Where(clause = "deleted = false")
@ToString(of = {"id", "hashId"})
@EqualsAndHashCode(of = "id", callSuper = false)
public class CKMetric extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "id")
    private long id;

    @Builder.Default
    @Column(name = "hash_id")
    private String hashId = generateHash();

    //Mediana
    @Column(name = "cbo")
    private double cbo;

    //Somatorio
    @Column(name = "loc")
    private double loc;

    //Maior valor
    @Column(name = "dit")
    private double dit;

    //Mediana
    @Column(name = "lcom")
    private double lcom;

    @OneToOne
    @JoinColumn(name = "fk_rpository")
    private Repository repository;
}
